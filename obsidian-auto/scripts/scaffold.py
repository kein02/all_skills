#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""obsidian-auto / scaffold.py

幂等地生成 Obsidian 知识库骨架：
  raw/ + wiki/{concepts,entities,sources} + AGENTS.md / README.md / index.md / log.md
并输出两个定时任务（每日整理 / 每周健康检查）的创建计划，
由 Agent 通过 automation_update 工具落地（脚本本身不调用任何外部 API）。

设计要点：
  - 只创建缺失项，绝不覆盖已有内容（--force 除外，且会先备份）；
  - 所有输出为 UTF-8 JSON，便于 Agent 解析；
  - dry-run 只出计划、不落盘；verify 只检查、不写入；
  - 重复调用结果一致（幂等）。

退出码：0 成功 / 2 参数校验失败 / 3 文件系统错误 / 4 verify 发现缺失。
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import sys
import unicodedata
from datetime import datetime
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

sys.path.insert(0, str(Path(__file__).resolve().parent))
from tasks import SKILL_NAME, build_tasks  # noqa: E402

SKILL_ROOT = Path(__file__).resolve().parent.parent
TEMPLATE_DIR = SKILL_ROOT / "assets" / "templates"
BASE_FILES = ["AGENTS.md", "README.md", "index.md", "log.md"]
BASE_TEMPLATES = {
    "AGENTS.md": "AGENTS.md.tpl",
    "README.md": "README.md.tpl",
    "index.md": "index.md.tpl",
    "log.md": "log.md.tpl",
}

EXIT_OK = 0
EXIT_VALIDATION = 2
EXIT_FS = 3
EXIT_VERIFY_MISSING = 4

CATEGORY_LABELS = {"concepts": "概念页", "entities": "实体页", "sources": "来源页"}
DEFAULT_CATEGORY_DESC = {
    "concepts": "按主题汇总的概念、方法与观点",
    "entities": "按对象汇总的工具、人物与平台信息",
    "sources": "每份原始资料一份摘要与出处",
}
RESERVED_NAMES = {"raw", "index", "log", "agents", "readme", "wiki"}

SECTION_CONCEPTS = """### wiki/concepts/：同一主题持续汇总

- 按概念、方法或问题组织页面，例如「核心概念」「方法步骤」「常见问题」，综合多份资料，不按文章逐篇复制摘要。
- 新资料涉及已有主题时，把有用内容补进对应章节；确实是新主题才建页，不因名称不同重复建页。
- 方法页写清步骤、适用条件和案例，重要内容链接到相应来源页；不同观点分别保留出处。"""

SECTION_ENTITIES = """### wiki/entities/：同一对象集中记录

- 按工具、人物、平台或组织建立页面，汇总资料中与该对象相关的用途、操作和案例。
- 同一对象的简称、别名归到同一页；新资料补充原页，涉及版本差异时注明版本或日期。
- 实体页链接到相关概念、方法和来源页，不把通用方法全文重复放进每个实体页。"""

SECTION_SOURCES = """### wiki/sources/：一份资料一份摘要

- 先为每份新增资料建立来源页，记录标题、作者、原文链接、raw 文件路径、日期、核心内容与适用条件。缺少的信息标为未提供，不补造。
- 同一份资料发生变化时，更新原有来源页，不重复新建。个人笔记标明是个人理解或实践记录。
- 来源页链接到从这份资料整理出的其他分类页，方便查看资料被用到了哪里。"""

SECTION_GENERIC = """### wiki/{cat}/：{desc}

- 按「{desc}」组织页面，综合多份资料写成一篇，不按文章逐篇复制摘要。
- 新资料涉及已有主题时补进对应章节；确实是新主题才建页，不因名称不同重复建页。
- 页面写清适用条件与案例，重要内容链接到相应来源页，不同观点分别保留出处。"""

DAY_CN = {"MO": "一", "TU": "二", "WE": "三", "TH": "四", "FR": "五", "SA": "六", "SU": "日"}
TIME_RE = re.compile(r"^([01]\d|2[0-3]):([0-5]\d)$")
CATEGORY_RE = re.compile(r"^[a-z0-9][a-z0-9_-]{0,30}$")
BAD_NAME_CHARS = set('<>:"/\\|?*')


class ValidationError(Exception):
    def __init__(self, messages):
        super().__init__("; ".join(messages))
        self.messages = messages


def emit(payload, code):
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    sys.exit(code)


def display_width(text):
    return sum(2 if unicodedata.east_asian_width(ch) in ("W", "F") else 1 for ch in text)


def padded(prefix, path_text, note, col=34):
    line = prefix + path_text
    return line + " " * max(2, col - display_width(line)) + note


def parse_args(argv=None):
    p = argparse.ArgumentParser(
        prog="scaffold.py",
        description="幂等地搭建 Obsidian 知识库骨架，并输出定时任务创建计划。",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "示例：\n"
            '  python scaffold.py --path "D:/Obsidian WH/AI学术论文写作" --name "AI学术论文写作" '
            '--domain "AI 学术论文写作" --material-desc "论文、写作指南、投稿经验、笔记"\n'
            '  python scaffold.py --path "D:/Notes" --profile minimal --automations off\n'
            '  python scaffold.py --path "D:/Notes" --extra-category "topics:主题页"\n'
            '  python scaffold.py --path "D:/Notes" --dry-run\n'
            '  python scaffold.py --path "D:/Notes" --verify\n'
        ),
    )
    p.add_argument("--path", required=True, help="仓库绝对路径（必填）")
    p.add_argument("--name", help="仓库名称，默认取路径最后一段")
    p.add_argument("--domain", default="通用知识管理", help="主题名称，用于文案，默认「通用知识管理」")
    p.add_argument("--material-desc", default="文章、论文、笔记", help="raw/ 里放什么，默认「文章、论文、笔记」")
    p.add_argument("--profile", choices=["standard", "minimal"], default="standard",
                   help="standard=raw+wiki 三个分类；minimal=只有 raw+wiki/sources")
    p.add_argument("--concept-desc")
    p.add_argument("--entity-desc")
    p.add_argument("--source-desc")
    p.add_argument("--extra-category", action="append", default=[],
                   help='追加分类，格式 "名称:说明"，可重复，如 --extra-category "topics:主题页"')
    p.add_argument("--automations", choices=["on", "off"], default="on", help="是否输出定时任务计划，默认 on")
    p.add_argument("--daily-time", help="每日整理时间 HH:MM（由用户指定，无默认值）")
    p.add_argument("--weekly-day", default="MO", help="每周健康检查星期（MO..SU），默认 MO")
    p.add_argument("--weekly-time", help="每周健康检查时间 HH:MM（由用户指定，无默认值）")
    p.add_argument("--date", help="写日志用的日期 YYYY-MM-DD，默认今天")
    p.add_argument("--dry-run", action="store_true", help="只输出计划，不创建任何东西")
    p.add_argument("--verify", action="store_true", help="只检查骨架是否完整，不写入")
    p.add_argument("--force", action="store_true", help="覆盖已存在的四份基础文件（先备份为 *.bak-时间戳）")
    p.add_argument("--create-parents", action="store_true", help="父目录不存在时一并创建")
    p.add_argument("--json", action="store_true", help="兼容参数；输出始终为 JSON")
    return p.parse_args(argv)


def validate(args):
    errors, warnings = [], []

    raw_path = (args.path or "").strip()
    if not raw_path:
        raise ValidationError(["--path 不能为空"])
    if not os.path.isabs(raw_path):
        raise ValidationError([f"--path 必须是绝对路径，收到：{raw_path}"])
    path = os.path.normpath(os.path.abspath(raw_path))
    if Path(path).drive and Path(path).parent == Path(path):
        raise ValidationError([f"--path 不能是磁盘根目录：{path}"])
    if Path(path).exists() and not Path(path).is_dir():
        raise ValidationError([f"--path 已存在但不是目录：{path}"])
    parent = Path(path).parent
    if not parent.exists() and not args.create_parents:
        raise ValidationError([f"父目录不存在：{parent}（如需自动创建请加 --create-parents）"])

    name = (args.name or Path(path).name).strip()
    if not name:
        raise ValidationError(["--name 无效，且无法从路径推导仓库名称"])
    if any(ch in BAD_NAME_CHARS for ch in name):
        errors.append(f"--name 含非法字符：{name}")

    domain = (args.domain or "").strip()
    if not domain:
        errors.append("--domain 不能为空")
    material = (args.material_desc or "").strip()
    if not material:
        errors.append("--material-desc 不能为空")

    base_cats = ["concepts", "entities", "sources"] if args.profile == "standard" else ["sources"]
    cats, descs = [], {}
    for c in base_cats:
        cats.append(c)
        descs[c] = DEFAULT_CATEGORY_DESC[c]
    for key, cat in (("concept_desc", "concepts"), ("entity_desc", "entities"), ("source_desc", "sources")):
        val = getattr(args, key)
        if val:
            if cat in cats:
                descs[cat] = val.strip()
            else:
                warnings.append(f"--{key.replace('_', '-')} 在当前 profile 下不适用（无 {cat} 分类），已忽略")
    for item in args.extra_category:
        if ":" not in item:
            errors.append(f"--extra-category 格式应为 名称:说明，收到：{item}")
            continue
        cname, cdesc = item.split(":", 1)
        cname, cdesc = cname.strip().lower(), cdesc.strip()
        if not CATEGORY_RE.match(cname):
            errors.append(f"分类名不合法（小写字母/数字/-/_，1-31 位）：{cname or '(空)'}")
            continue
        if cname in RESERVED_NAMES:
            errors.append(f"分类名与保留名冲突：{cname}")
            continue
        if cname in cats:
            warnings.append(f"分类 {cname} 已存在，已忽略重复的 --extra-category")
            continue
        if not cdesc:
            errors.append(f"分类 {cname} 缺少说明")
            continue
        cats.append(cname)
        descs[cname] = cdesc

    times_required = args.automations == "on" and not args.verify
    for flag, val in (("--daily-time", args.daily_time), ("--weekly-time", args.weekly_time)):
        if not val:
            if times_required:
                errors.append(f"{flag} 必须由用户指定（不提供默认时间），例如 {flag} 09:00")
            continue
        if not TIME_RE.match(val):
            errors.append(f"{flag} 需为 HH:MM（00:00-23:59），收到：{val}")
    if args.weekly_day not in DAY_CN:
        errors.append(f"--weekly-day 需为 MO/TU/WE/TH/FR/SA/SU，收到：{args.weekly_day}")

    date = args.date
    if date:
        try:
            datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            errors.append(f"--date 需为 YYYY-MM-DD，收到：{date}")
    else:
        date = datetime.now().strftime("%Y-%m-%d")

    if errors:
        raise ValidationError(errors)

    return {
        "path": path,
        "name": name,
        "domain": domain,
        "material": material,
        "profile": args.profile,
        "categories": cats,
        "descs": descs,
        "date": date,
        "automations_enabled": args.automations == "on",
        "daily_time": args.daily_time,
        "weekly_day": args.weekly_day,
        "weekly_time": args.weekly_time,
        "create_parents": args.create_parents,
        "warnings": warnings,
    }


def expected_dirs(cfg):
    vault = Path(cfg["path"])
    return [vault, vault / "raw", vault / "wiki"] + [vault / "wiki" / c for c in cfg["categories"]]


def build_tree(cfg):
    cats, descs = cfg["categories"], cfg["descs"]
    lines = [f"{cfg['name']}/"]
    lines.append(padded("├── ", "raw/", f"原始资料：{cfg['material']}等，事实的源头"))
    lines.append("├── wiki/")
    for i, c in enumerate(cats):
        prefix = "│   └── " if i == len(cats) - 1 else "│   ├── "
        label = CATEGORY_LABELS.get(c, "分类页")
        lines.append(padded(prefix, f"{c}/", f"{label}：{descs[c]}"))
    root = [("AGENTS.md", "AI 工作规范（相当于\"员工手册\"）"),
            ("index.md", "全库目录与索引，AI 自己维护"),
            ("log.md", "干活日志，AI 自己记"),
            ("README.md", "本说明（知识库地图）")]
    for i, (fn, note) in enumerate(root):
        prefix = "└── " if i == len(root) - 1 else "├── "
        lines.append(padded(prefix, fn, note))
    return "\n".join(lines)


def build_flow(cfg):
    cats = cfg["categories"]
    others = [c for c in cats if c != "sources"]
    lines = ["raw/（原始资料，只读）", "        ↓  提炼、关联、去重", "wiki/sources/（这份资料讲了什么）"]
    if others:
        if "concepts" in others and "entities" in others:
            lines.append("        ↓  按主题归并        ↓  按对象归并")
            lines.append("wiki/concepts/（概念、方法）   wiki/entities/（工具、平台、人物）")
        elif len(others) == 1:
            label = CATEGORY_LABELS.get(others[0], "分类页")
            lines.append("        ↓  按分类归并")
            lines.append(f"wiki/{others[0]}/（{label}）")
        else:
            lines.append("        ↓  按分类归并")
            lines.append("   ".join(f"wiki/{c}/（{CATEGORY_LABELS.get(c, '分类页')}）" for c in others))
        lines.append("        ↓  页面之间以双链互相连接")
    else:
        lines.append("        ↓  摘要即成品，原件留档")
    lines.append("index.md（全库导航）   +   log.md（每次改了什么）")
    return "\n".join(lines)


def build_category_rows_agents(cfg):
    rows = [f"| raw/ | 原始资料（{cfg['material']}） | 只读 |"]
    rows += [f"| wiki/{c}/ | {cfg['descs'][c]} | 可写 |" for c in cfg["categories"]]
    rows += ["| index.md | 全库知识导航与索引 | 可写 |",
             "| log.md | 操作日志 | 追加写 |",
             "| AGENTS.md | 本工作规范 | 需用户确认后修改 |"]
    return "\n".join(rows)


def build_category_rows_readme(cfg):
    rows = [f"| `raw/` | **原始资料区。** 存放{cfg['material']}等未经加工的一手材料，是事实的源头。"
            f"AI 只负责读，任何加工结果都不能回写到这里。 | 用户投喂 | **只读** |"]
    for c in cfg["categories"]:
        label = CATEGORY_LABELS.get(c, "分类页")
        tail = ("记录标题、作者、出处、核心内容与适用条件。"
                if c == "sources" else "综合多份资料写成一篇，而不是一篇原文对应一篇。")
        rows.append(f"| `wiki/{c}/` | **{label}。** {cfg['descs'][c]}。{tail} | AI | 可写 |")
    rows += ["| `index.md` | **全库目录。** 知识导航与索引，负责把散落的页面组织成可查的地图。"
             "每次整理后由 AI 同步更新。 | AI | 可写 |",
             "| `log.md` | **干活日志。** 记录每次操作的时间、处理来源、改动页面、主要变化、待确认问题，"
             "也是判断\"哪些资料已处理过\"的基线。 | AI | 追加写 |",
             "| `AGENTS.md` | **工作规范。** 目录约定、整理规则、冲突处理、查询规则、边界红线，"
             "AI 每次任务开始前先读它。 | 用户主导 | 需用户确认后修改 |"]
    return "\n".join(rows)


def build_category_rows_index(cfg):
    rows = [f"| `raw/` | 原始资料（{cfg['material']}），只读，事实源头 |"]
    rows += [f"| `wiki/{c}/` | {cfg['descs'][c]} |" for c in cfg["categories"]]
    rows.append("| `log.md` | 操作日志，记录每次改动 |")
    return "\n".join(rows)


def build_index_headings(cfg):
    blocks = []
    for c in cfg["categories"]:
        label = CATEGORY_LABELS.get(c, "分类页")
        blocks.append(f"### {label}（wiki/{c}/）\n\n_暂无页面。_")
    return "\n\n".join(blocks)


def build_stats_line(cfg):
    parts = []
    for c in cfg["categories"]:
        label = CATEGORY_LABELS.get(c, "分类页").replace("页", "")
        parts.append(f"{label} 0")
    parts.append(f"最近更新：{cfg['date']}")
    return " ｜ ".join(parts)


def build_sections(cfg):
    out = []
    for c in cfg["categories"]:
        if c == "concepts":
            out.append(SECTION_CONCEPTS)
        elif c == "entities":
            out.append(SECTION_ENTITIES)
        elif c == "sources":
            out.append(SECTION_SOURCES)
        else:
            out.append(SECTION_GENERIC.format(cat=c, desc=cfg["descs"][c]))
    return "\n\n".join(out)


def build_automation_rows(cfg):
    if not cfg["automations_enabled"]:
        return "| — | — | 未启用定时任务，需要时手动整理 |"
    day = DAY_CN[cfg["weekly_day"]]
    return "\n".join([
        f"| 知识库每日整理 | 每天 {cfg['daily_time']} | "
        f"读 `AGENTS.md` → 对照 `log.md` 检查 `raw/` 有无新增/变化 → 有则整理进 `wiki/` 并更新 "
        f"`index.md`、`log.md`；没有则直接结束 |",
        f"| 知识库每周健康检查 | 每周{day} {cfg['weekly_time']} | "
        f"找出无效双链、孤立页面、结论冲突的知识页，整理成清单等用户确认；**检查阶段不改任何文件** |",
    ])


def build_entry_note(cfg):
    if [c for c in cfg["categories"] if c != "sources"]:
        return "一份资料进来，通常会在几处留下痕迹：`sources/` 留摘要，其余分类目录补内容，彼此用双链关联。"
    return "一份资料进来，先在 `sources/` 留一页摘要，原件原样留在 `raw/` 备查，两者以双链互相指向。"


def build_log_summary(cfg):
    cats = "、".join(f"wiki/{c}/" for c in cfg["categories"])
    return (f"处理来源：skill `obsidian-auto` 初始化本仓库｜改动页面：新建目录 raw/、{cats}；"
            f"新建 AGENTS.md、README.md、index.md、log.md｜主要变化：按 {cfg['profile']} 结构搭建骨架，"
            f"分类为 {'、'.join(cfg['categories'])}；全库暂无知识页，等待首批资料入库。｜待确认问题：无。")


def render_context(cfg):
    return {
        "{{VAULT_NAME}}": cfg["name"],
        "{{DOMAIN}}": cfg["domain"],
        "{{MATERIAL_DESC}}": cfg["material"],
        "{{DATE}}": cfg["date"],
        "{{TIME}}": datetime.now().strftime("%H:%M"),
        "{{TREE}}": build_tree(cfg),
        "{{FLOW_DIAGRAM}}": build_flow(cfg),
        "{{ENTRY_NOTE}}": build_entry_note(cfg),
        "{{CATEGORY_ROWS_AGENTS}}": build_category_rows_agents(cfg),
        "{{CATEGORY_ROWS_README}}": build_category_rows_readme(cfg),
        "{{CATEGORY_ROWS_INDEX}}": build_category_rows_index(cfg),
        "{{CATEGORY_INDEX_HEADINGS}}": build_index_headings(cfg),
        "{{CATEGORY_SECTIONS}}": build_sections(cfg),
        "{{AUTOMATION_ROWS}}": build_automation_rows(cfg),
        "{{STATS_LINE}}": build_stats_line(cfg),
        "{{LOG_SUMMARY}}": build_log_summary(cfg),
    }


def render_file(filename, ctx):
    tpl_path = TEMPLATE_DIR / BASE_TEMPLATES[filename]
    if not tpl_path.is_file():
        raise FileNotFoundError(f"模板缺失：{tpl_path}")
    text = tpl_path.read_text(encoding="utf-8")
    for key, val in ctx.items():
        text = text.replace(key, val)
    leftovers = re.findall(r"\{\{[A-Z_]+\}\}", text)
    if leftovers:
        raise ValueError(f"{filename} 存在未替换占位符：{sorted(set(leftovers))}")
    return text


def build_automations(cfg):
    if not cfg["automations_enabled"]:
        return []
    return [
        {**task, "scheduleType": "recurring", "status": "ACTIVE", "cwd": cfg["path"]}
        for task in build_tasks(
            path=cfg["path"],
            name=cfg["name"],
            categories=cfg["categories"],
            daily_time=cfg["daily_time"],
            weekly_day=cfg["weekly_day"],
            weekly_time=cfg["weekly_time"],
        )
    ]


def verify(cfg):
    missing_dirs = [str(d) for d in expected_dirs(cfg) if not d.is_dir()]
    vault = Path(cfg["path"])
    missing_files = [str(vault / f) for f in BASE_FILES if not (vault / f).is_file()]
    ok = not missing_dirs and not missing_files
    payload = {
        "ok": ok,
        "mode": "verify",
        "vault": {"path": cfg["path"], "name": cfg["name"]},
        "missing_dirs": missing_dirs,
        "missing_files": missing_files,
        "summary_lines": ["✅ 骨架完整" if ok else "⚠️ 骨架不完整，建议去掉 --verify 重新执行以补齐"],
    }
    emit(payload, EXIT_OK if ok else EXIT_VERIFY_MISSING)


def execute(cfg, dry_run):
    vault = Path(cfg["path"])
    created_dirs, existing_dirs = [], []
    created_files, skipped_files, backed_up = [], [], []
    warnings = list(cfg["warnings"])

    plan_dirs = expected_dirs(cfg)
    if dry_run:
        for d in plan_dirs:
            (existing_dirs if d.is_dir() else created_dirs).append(str(d))
    else:
        vault_created = False
        if not vault.exists():
            vault.mkdir(parents=cfg["create_parents"])
            vault_created = True
        for d in plan_dirs:
            if d == vault and vault_created:
                created_dirs.append(str(d))
            elif d.is_dir():
                existing_dirs.append(str(d))
            else:
                d.mkdir(parents=True, exist_ok=True)
                created_dirs.append(str(d))

    ctx = render_context(cfg)
    for fn in BASE_FILES:
        target = vault / fn
        exists = target.is_file()
        if dry_run:
            (skipped_files if exists else created_files).append(str(target))
            continue
        if exists and not cfg.get("force"):
            skipped_files.append(str(target))
            continue
        if exists:
            ts = datetime.now().strftime("%Y%m%d-%H%M%S")
            backup = target.with_name(f"{fn}.bak-{ts}")
            shutil.copy2(target, backup)
            backed_up.append(str(backup))
        target.write_text(render_file(fn, ctx), encoding="utf-8", newline="\n")
        created_files.append(str(target))

    changed = bool(created_dirs or created_files or backed_up)
    summary = []
    if dry_run:
        summary.append(f"[dry-run] 将创建 {len(created_dirs)} 个目录、{len(created_files)} 个文件；"
                       f"已存在 {len(existing_dirs)} 个目录、{len(skipped_files)} 个文件")
    else:
        summary.append(f"目录：新建 {len(created_dirs)} 个，已存在 {len(existing_dirs)} 个")
        summary.append(f"文件：新建 {len(created_files)} 个，跳过 {len(skipped_files)} 个"
                       + (f"，备份 {len(backed_up)} 个" if backed_up else ""))
        summary.append("结果：" + ("已就绪（本次有变更）" if changed else "已就绪（无变更，幂等）"))
    summary.append(f"结构：{cfg['profile']}（{', '.join(cfg['categories'])}）")

    return {
        "ok": True,
        "mode": "dry-run" if dry_run else "apply",
        "vault": {"path": cfg["path"], "name": cfg["name"], "domain": cfg["domain"]},
        "structure": {"profile": cfg["profile"], "categories": cfg["categories"]},
        "created_dirs": created_dirs,
        "existing_dirs": existing_dirs,
        "created_files": created_files,
        "skipped_files": skipped_files,
        "backed_up": backed_up,
        "changed": changed,
        "automations": build_automations(cfg),
        "summary_lines": summary,
        "warnings": warnings,
    }


def main(argv=None):
    args = parse_args(argv)
    try:
        cfg = validate(args)
    except ValidationError as exc:
        emit({"ok": False, "error": {"code": "validation", "messages": exc.messages}}, EXIT_VALIDATION)
        return
    cfg["force"] = args.force

    if args.verify:
        verify(cfg)
        return

    try:
        result = execute(cfg, args.dry_run)
    except (OSError, ValueError, FileNotFoundError) as exc:
        emit({"ok": False, "error": {"code": "fs", "messages": [str(exc)]}}, EXIT_FS)
        return
    emit(result, EXIT_OK)


if __name__ == "__main__":
    main()
