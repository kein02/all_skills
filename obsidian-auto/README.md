# obsidian-auto

[English](README.en.md) | 简体中文

一个 Agent Skill：一句话给 Obsidian 建好 `raw/` + `wiki/` 三层知识库骨架，并按你指定的时间挂上「每日整理」「每周健康检查」两个定时任务——重复执行只补缺失，不覆盖你已有的内容。

![type](https://img.shields.io/badge/type-agent--skill-blue) ![scope](https://img.shields.io/badge/scope-personal-green)

## 它解决什么问题

用 Obsidian 做知识库，卡住的地方通常不是软件，而是三件事：

- **结构从零搭太烦**——建目录、写规范、定页面格式，折腾半小时还没放进去一篇资料；
- **建完没人维护**——资料堆在 `raw/` 里没人整理，两个月后自己都不想打开；
- **换个 Agent 又要重来**——在 Claude Code 里配好的东西，换到 Codex 得再折腾一遍。

这个 skill 把「骨架 + 维护任务」一起打包：一条命令生成目录与四份规范文件（`AGENTS.md`、`README.md`、`index.md`、`log.md`），再把每日整理、每周健康检查挂到调度器上；同一份技能可以装进 12 个 Agent。

## 安装

不同 Agent 工具安装方式不同；如在多个工具中使用，请分别安装。以下任选一种：

**一键脚本**（拷入 `~/.agents/skills/`，旧版自动备份）：

```bash
curl -fsSL https://raw.githubusercontent.com/kein02/all_skills/main/install.sh | bash -s -- obsidian-auto
```

**社区 CLI**（skills.sh，支持多种 agent 工具）：

```bash
npx skills add kein02/all_skills -s obsidian-auto
```

**手动**（项目级安装也用这种：放进 `<项目>/.agents/skills/` 即可）：

```bash
git clone --depth 1 https://github.com/kein02/all_skills
mkdir -p ~/.agents/skills && cp -r all_skills/obsidian-auto ~/.agents/skills/
```

> [!IMPORTANT]
> 安装后需**新开一个会话**才生效（skills 目录在会话启动时扫描），当前会话可用 `/obsidian-auto` 强制调用。

**验证**：新会话说一句

> 用 obsidian-auto 在 `D:/Obsidian/读书笔记` 建个知识库，每天 8 点整理，每周日晚上 9 点检查

能自动进入工作流即安装成功。

**更新**：重跑同一条安装命令（旧版自动备份为 `obsidian-auto.bak.<时间戳>`）。

**依赖**：Python 3.8+，只用标准库，无需 pip；Windows / macOS / Linux 均可。

## 使用方法

**自动触发**——包含以下意思的说法会自动激活：

- "新建一个 Obsidian 知识库"
- "照 AI学习知识库 那样给我建一个库"
- "知识库结构乱了 / 缺目录，帮我补齐"
- "给这个知识库加每日整理和每周检查"

**手动调用**——在支持斜杠命令的宿主里输入 `/obsidian-auto`（Codex 用 `$obsidian-auto`）。

## 它会生成什么

```
你的知识库/
├── raw/                       原始资料：文章、论文、笔记，只读
├── wiki/
│   ├── concepts/              概念页：方法、观点，按主题汇总
│   ├── entities/              实体页：工具、人物、平台，按对象汇总
│   └── sources/               来源页：一份资料一份摘要
├── AGENTS.md                  AI 工作规范（每次任务前必读）
├── index.md                   全库目录，AI 维护
├── log.md                     操作日志，增量基线
└── README.md                  给你看的地图
```

两个定时任务，时间全部由你指定：

| 任务 | 做什么 | 时间 |
|---|---|---|
| 每日整理 | 读 `AGENTS.md`，对照 `log.md` 找 `raw/` 里新增或变化的文件，整理进 `wiki/` 并更新 `index.md`、`log.md`；没有变化就直接结束 | 每天，你指定的时刻 |
| 每周健康检查 | 扫无效双链、孤立页面、结论冲突的页面，出清单等你确认；**检查阶段不改任何文件** | 每周，你指定的星期与时刻 |

> 时间没有默认值。没说明就问你，不会替你拍板。

## 命令参考

### `scaffold.py`——建结构

| 参数 | 说明 |
|---|---|
| `--path` | 仓库绝对路径（必填） |
| `--name` / `--domain` / `--material-desc` | 仓库名、主题、`raw/` 内容说明，决定全部文案 |
| `--daily-time` / `--weekly-time` | **必填**，触发时间 |
| `--weekly-day` | 每周任务的星期，默认 `MO` |
| `--profile` | `standard`（三个分类）或 `minimal`（只要 sources） |
| `--extra-category "名称:说明"` | 追加自定义分类，可重复 |
| `--automations off` | 只要结构，不排任务 |
| `--dry-run` / `--verify` / `--force` / `--create-parents` | 预演 / 体检 / 覆盖前备份 / 建父目录 |

```bash
python scripts/scaffold.py --path "D:/Obsidian WH/新库" --name "新库" --domain "AI 学习" \
  --daily-time "08:00" --weekly-day SU --weekly-time "21:00"
```

输出为 JSON：`created_files`、`skipped_files`、`changed`、`automations`、`summary_lines`。

### `schedule.py`——把任务挂到调度器

| 平台 | 产物 |
|---|---|
| `workbuddy` | `automation_update` 所需的 JSON |
| `cron` | `crontab.txt` + 包装脚本 |
| `schtasks` | Windows 计划任务注册脚本（`.ps1`，UTF-8 BOM）+ `.cmd` 包装 |
| `launchd` | macOS LaunchAgent plist |
| `json` | 与平台无关的任务规格，含 prompt 全文 |

```bash
python scripts/schedule.py --vault "D:/Obsidian WH/新库" --platform auto \
  --daily-time "08:00" --weekly-day SU --weekly-time "21:00" --write
```

`auto` 按操作系统选（Windows→计划任务、macOS→launchd、Linux→cron），`--runner` 指定用哪个 CLI 执行任务（默认 `claude -p`）。

### `install.py`——装到别的 Agent

```bash
python scripts/install.py --target all --scope user           # 装到本机所有支持的宿主
python scripts/install.py --target cursor --scope project --project "D:/repo"
```

支持 `claude` `codex` `cursor` `gemini` `copilot` `windsurf` `cline` `roo` `opencode` `goose` `kiro` `workbuddy`，或 `all`。内容一致判 `unchanged` 跳过，有差异需 `--force` 且先备份。

## 幂等与安全

- **只增不改**：已存在的目录与文件一律跳过，`raw/` 与已有知识页完全不触碰；
- **覆盖要备份**：只有显式 `--force` 才会覆盖四份规范文件，且先生成 `*.bak-<时间戳>`；
- **时间你说了算**：`--daily-time` / `--weekly-time` 缺省直接报错（退出码 2），不会偷偷排到某个时刻；
- **不静默改系统**：cron / 计划任务 / launchd 属于对机器的持久改动，先展示命令、经你确认再注册；
- **重复执行安全**：第二次运行返回 `changed=false`，不产生重复日志或重复任务。

## 跨 Agent 兼容

遵循开放 Agent Skills 规范，只依赖 `name` + `description` 两个 frontmatter 字段，拷过去就能用。

| 宿主 | 技能目录 | 调用 |
|---|---|---|
| Claude Code | `~/.claude/skills/` | `/obsidian-auto` |
| Codex CLI | `~/.codex/skills/` | `$obsidian-auto` |
| Cursor | `~/.cursor/skills/` | 描述触发（装完需重载窗口） |
| WorkBuddy | `~/.workbuddy/skills/` | 描述触发 |
| 其他（Gemini / Copilot / Windsurf / Cline / Roo / OpenCode / Goose / Kiro） | 见 `references/agent-compat.md` | 描述触发 |

## 文件结构

```
obsidian-auto/
├── SKILL.md                    入口：触发条件 + 6 步工作流
├── scripts/
│   ├── scaffold.py             幂等骨架生成器（校验 / dry-run / verify / force）
│   ├── schedule.py             调度生成器（workbuddy / cron / schtasks / launchd / json）
│   ├── install.py              多宿主安装器
│   └── tasks.py                两个任务的共享定义（prompt / 时间）
├── assets/templates/           AGENTS / README / index / log 四份模板
└── references/
    ├── parameters.md           完整参数、退出码、幂等与对账规则
    └── agent-compat.md         各 Agent 目录、字段与调用差异
```

## 已知边界

- 只建骨架，**不搬运内容**——资料要你自己放进 `raw/`，之后由每日任务整理；
- 任务 prompt 内嵌仓库绝对路径，**移动仓库后需重跑**以更新；
- 系统级调度依赖本机装有对应 CLI（`claude -p`、`codex exec`、`gemini -p`），且该 CLI 需能从 stdin 读指令；
- Windows 计划任务注册需管理员 PowerShell；
- Obsidian 新建仓库自带的 `欢迎.md` 不会被自动删除，只提示你处理；
- 生成为「学术版 / 通用版」文案，行业术语差异靠 `--domain`、`--material-desc` 调整，不提供每个领域的专用模板。

## 反馈与改进

用出问题（结构不合预期、任务没挂上、某宿主触发不灵）直接在本仓库提 issue，附上当时的命令与输出 JSON，便于定位。
