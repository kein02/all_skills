#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""obsidian-auto / install.py

把本技能安装到主流 agent 的技能目录（个人级或项目级）。
各宿主的目录约定不同，本脚本集中维护映射，避免手动拷贝出错。

用法：
  python install.py --target workbuddy
  python install.py --target all --scope user --dry-run
  python install.py --target claude,cursor --scope project --project "D:/repo"
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import sys
from datetime import datetime
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

SKILL_ROOT = Path(__file__).resolve().parent.parent
SKILL_NAME = SKILL_ROOT.name

# 个人级 / 项目级技能目录（依据 2026 年各客户端公开约定，见 references/agent-compat.md）
TARGETS = {
    "claude":    {"user": "~/.claude/skills",              "project": ".claude/skills"},
    "codex":     {"user": "~/.codex/skills",               "project": ".codex/skills"},
    "cursor":    {"user": "~/.cursor/skills",              "project": ".cursor/skills"},
    "gemini":    {"user": "~/.gemini/skills",              "project": ".gemini/skills"},
    "copilot":   {"user": "~/.copilot/skills",             "project": ".github/skills"},
    "windsurf":  {"user": "~/.codeium/windsurf/skills",    "project": ".windsurf/skills"},
    "cline":     {"user": "~/.agents/skills",              "project": ".agents/skills"},
    "roo":       {"user": "~/.roo/skills",                 "project": ".roo/skills"},
    "opencode":  {"user": "~/.config/opencode/skills",     "project": ".opencode/skills"},
    "goose":     {"user": "~/.config/goose/skills",        "project": ".goose/skills"},
    "kiro":      {"user": "~/.kiro/skills",                "project": ".kiro/skills"},
    "workbuddy": {"user": "~/.workbuddy/skills",           "project": ".workbuddy/skills"},
}

IGNORE = shutil.ignore_patterns("__pycache__", "*.pyc", "*.bak-*", ".DS_Store")


def emit(payload, code=0):
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    sys.exit(code)


def tree_digest(root):
    root = Path(root)
    items = []
    for p in sorted(root.rglob("*")):
        if p.is_file():
            items.append((p.relative_to(root).as_posix(),
                          hashlib.sha256(p.read_bytes()).hexdigest()))
    return hashlib.sha256(json.dumps(items, ensure_ascii=False).encode("utf-8")).hexdigest()


def install_one(target, scope, project, force, dry_run):
    mapping = TARGETS[target]
    if scope == "user":
        base = Path(os.path.expanduser(mapping["user"]))
    else:
        base = (Path(project).resolve() / mapping["project"])
    dest = base / SKILL_NAME

    if dest.exists() and dest.resolve() == SKILL_ROOT.resolve():
        return {"target": target, "scope": scope, "path": str(dest), "action": "self"}
    if dest.exists() and tree_digest(dest) == tree_digest(SKILL_ROOT):
        return {"target": target, "scope": scope, "path": str(dest), "action": "unchanged"}
    if dest.exists() and not force:
        return {"target": target, "scope": scope, "path": str(dest), "action": "conflict",
                "note": "目标已存在且内容不同，加 --force 覆盖（会先备份）"}

    action = "installed"
    if dry_run:
        return {"target": target, "scope": scope, "path": str(dest),
                "action": "would-" + ("replace" if dest.exists() else "install")}

    base.mkdir(parents=True, exist_ok=True)
    backup = None
    if dest.exists():
        backup = dest.with_name(f"{SKILL_NAME}.bak-{datetime.now().strftime('%Y%m%d-%H%M%S')}")
        shutil.move(str(dest), str(backup))
        action = "replaced"
    shutil.copytree(SKILL_ROOT, dest, ignore=IGNORE)
    return {"target": target, "scope": scope, "path": str(dest), "action": action,
            "backup": str(backup) if backup else None}


def main(argv=None):
    p = argparse.ArgumentParser(prog="install.py", description="安装 obsidian-auto 到各 agent 技能目录")
    p.add_argument("--target", default="workbuddy",
                   help="目标宿主：all 或 " + "/".join(TARGETS) + "，可用逗号分隔多个")
    p.add_argument("--scope", choices=["user", "project"], default="user")
    p.add_argument("--project", help="--scope project 时的项目根目录")
    p.add_argument("--force", action="store_true", help="覆盖已存在的同名技能（先备份）")
    p.add_argument("--dry-run", action="store_true")
    args = p.parse_args(argv)

    names = [n.strip().lower() for n in args.target.split(",") if n.strip()]
    if "all" in names:
        names = list(TARGETS)
    unknown = [n for n in names if n not in TARGETS]
    if unknown:
        emit({"ok": False, "error": {"code": "validation",
                                     "messages": [f"未知目标：{', '.join(unknown)}"]}}, 2)
    if args.scope == "project" and not args.project:
        emit({"ok": False, "error": {"code": "validation",
                                     "messages": ["--scope project 需要 --project 指定项目目录"]}}, 2)
    if args.scope == "project" and not Path(args.project).is_dir():
        emit({"ok": False, "error": {"code": "validation",
                                     "messages": [f"项目目录不存在：{args.project}"]}}, 2)

    results = [install_one(n, args.scope, args.project, args.force, args.dry_run) for n in names]
    summary = [f"{r['target']}: {r['action']} → {r['path']}" for r in results]
    emit({"ok": True, "skill": SKILL_NAME, "source": str(SKILL_ROOT),
          "scope": args.scope, "dry_run": args.dry_run,
          "results": results, "summary_lines": summary})


if __name__ == "__main__":
    main()
