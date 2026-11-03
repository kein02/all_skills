---
name: obsidian-auto
description: 按配置生成 Obsidian 知识库骨架（raw/ + wiki 分类目录 + AGENTS.md、README.md、index.md、log.md 四件套），并配置「每日整理 / 每周健康检查」两个定时任务（触发时间由用户指定，不设默认值）；支持 WorkBuddy 自动化工具、系统级 cron / Windows 计划任务 / macOS launchd 三种落地方式，可用一条命令安装到 Claude Code、Codex、Cursor、Copilot、Gemini CLI、Windsurf 等 agent。触发词：新建知识库、搭知识库、Obsidian 仓库、复刻知识库结构、知识库目录、每日整理任务、每周健康检查、raw wiki 结构。幂等：重复执行只补缺失，不覆盖已有文件，不重复建任务。
---

# Obsidian 知识库脚手架（obsidian-auto）

## 用途

把「raw 原始资料 → wiki 结构化知识页 → index/log 导航与日志」这套三层知识库结构，连同两个维护它的定时任务（每日整理、每周健康检查，时间由用户指定），按配置复现到任意路径，并适配不同 agent 的调度能力。主题差异全部通过参数调整，不改模板。

## 适用场景

- 从零新建 Obsidian 知识库，希望开箱即用、结构规范。
- 已有仓库结构不完整（缺 `raw/`、`wiki/sources/`、`AGENTS.md` 等），需要补齐。
- 给已有仓库接入「每日整理 + 每周健康检查 + 目录结构自检」的自动化。
- 复刻某个现有知识库的组织方式到新主题。
- 把同一套能力铺到多个 agent（Claude Code / Codex / Cursor / WorkBuddy 等）。

## 触发条件

用户表达以下任一意图时使用：

- 「新建 / 搭一个 Obsidian 知识库」「给我建个知识库」
- 「照 XX 知识库的结构建一个」「复刻这个仓库的结构」
- 「知识库缺目录 / 结构乱了，帮我补齐」
- 「给这个知识库加每日整理、每周检查的定时任务」
- 提供 Obsidian 仓库路径，并希望得到 `raw/`、`wiki/`、`AGENTS.md` 这套结构

不适用：仅编辑某个知识页、仅整理已有 raw 资料（那是每日任务的职责）、非 Obsidian 的笔记软件。

## 快速开始

```bash
python "scripts/scaffold.py" --path "D:/Obsidian WH/新知识库" \
  --name "新知识库" --domain "AI 学习" --material-desc "文章、论文、笔记" \
  --daily-time "08:00" --weekly-day SU --weekly-time "21:00"
```

`--daily-time` 与 `--weekly-time` 必须由用户给出；省略会被校验拦下（退出码 2）。

路径以技能目录为基准；不确定时取 SKILL.md 所在目录下的 `scripts/scaffold.py`。

## 参数

| 参数 | 默认 | 说明 |
| --- | --- | --- |
| `--path` | 必填 | 仓库绝对路径 |
| `--name` | 路径末段 | 仓库名，用于文案与任务命名 |
| `--domain` | 通用知识管理 | 主题名，写进 AGENTS.md 开头 |
| `--material-desc` | 文章、论文、笔记 | `raw/` 内容说明 |
| `--profile` | standard | `standard`=三个分类；`minimal`=仅 sources |
| `--concept-desc` / `--entity-desc` / `--source-desc` | 见 references | 覆盖分类说明 |
| `--extra-category` | 无 | `名称:说明`，可重复追加分类 |
| `--automations` | on | `off` 则不输出任务计划 |
| `--daily-time` / `--weekly-time` / `--weekly-day` | **必填 / 必填** / MO | 任务触发时间，必须由用户给出，不设默认值 |
| `--dry-run` / `--verify` | 关 | 只出计划 / 只检查 |
| `--force` | 关 | 覆盖四件套前先备份（需用户明确同意） |
| `--create-parents` | 关 | 自动创建父目录 |

调度与安装另有两条命令，完整参数见 `references/parameters.md`：

```bash
python "scripts/schedule.py" --vault "<已存在的库>" --platform auto --write
python "scripts/install.py"  --target all --scope user
```

## 工作流程

### 第 1 步：收集参数

必需：`--path`（用户没说就追问，禁止猜测路径）。其余按以下规则推导，并在最终汇报中写明假设：

- `--name`：取路径最后一段；`--domain`：去掉名称末尾的「知识库 / 库 / 仓库」后缀。
- `--material-desc`：按主题推断（学术写作→「论文、写作指南、投稿经验、笔记」；读书→「书摘、书评、笔记」）。
- 用户指定了分类需求（如「不要 entities」）→ `--profile minimal` 或调整 `--extra-category`。
- 用户指定了时间（如「每天 8 点」「每周日晚上 9 点」）→ 映射到 `--daily-time` / `--weekly-day` / `--weekly-time`。
- **时间没有默认值**：用户未说明时必须先问，问清「每日几点」「每周几几点」，不得自行决定，也不要用示例时间代替。

### 第 2 步：先 dry-run 校验

```bash
python "scripts/scaffold.py" --path "<绝对路径>" ... --dry-run
```

- `ok=false` 读 `error.messages` 修正参数，不要落盘。
- `ok=true` 检查 `warnings`（时间冲突、无效参数被忽略），需要时向用户确认。

### 第 3 步：正式执行

去掉 `--dry-run` 重跑同一条命令。关注输出：`created_dirs` / `created_files` 为新建，`skipped_files` 为已存在未改动，`changed=false` 表示结构本就完整。

不要使用 `--force`，除非用户明确要求覆盖已有规范文件；使用时先告知会生成 `*.bak-<时间戳>`。

### 第 4 步：配置定时任务（按宿主适配）

先判断当前宿主能力，再选落地方式：

| 情况 | 做法 |
| --- | --- |
| 宿主提供自动化工具（如 WorkBuddy 的 `automation_update`） | 用 `scaffold.py` 输出里的 `automations` 数组，逐个 create / update |
| 无自动化工具（Claude Code、Codex、Cursor 等） | 运行 `schedule.py --platform auto --write`，生成包装脚本与调度文件，**经用户确认后**再注册 |
| 只需要留档、暂不调度 | `schedule.py --platform json --write`，产物写到 `.obsidian-auto/tasks.json` |

宿主自动化工具的**幂等对账规则**（同名同路径为键）：

| 现有状态 | 动作 |
| --- | --- |
| 同名同 cwd，rrule 与 prompt 一致 | 跳过 |
| 同名同 cwd，rrule 或 prompt 不同 | 更新该任务 |
| 同 cwd 存在名称相近的任务 | 暂停，问用户是否重复，勿自动创建 |
| 同名任务在别的 cwd | 新建（名称已含仓库名，天然区分） |
| 完全不存在 | 创建 |

系统级调度（cron / 计划任务 / launchd）属于对机器的持久改动：**先展示生成内容与命令，得到用户同意再执行**。首次配置前确认 `--runner` 指向的命令确实存在，例如 `claude -p`、`codex exec`、`gemini -p`。

### 第 5 步：校验与收尾

```bash
python "scripts/scaffold.py" --path "<绝对路径>" --verify
```

`ok=true` 才算完成；否则重跑一次落库命令补齐。

若仓库根目录存在 `欢迎.md`（Obsidian 新建仓库自带），不要自动删除，在汇报中提示用户是否删除。

### 第 6 步：汇报

按以下结构输出，不要省略：

- 结构：路径、`profile`、实际分类列表；
- 文件：新建 / 跳过 / 备份清单；
- 定时任务：任务名 + 频率 + 状态（新建 / 已存在跳过 / 已更新 / 待用户确认）；
- 下一步：用 Obsidian 打开该文件夹；把资料放进 `raw/`；`欢迎.md` 待确认项；
- 如用了默认值或推断值，明确写出假设。

## 安装到其他 agent

```bash
python "scripts/install.py" --target all --scope user          # 铺到本机所有已支持的宿主
python "scripts/install.py" --target claude,codex --scope user
python "scripts/install.py" --target cursor --scope project --project "D:/repo"
```

支持的目标：`claude` `codex` `cursor` `gemini` `copilot` `windsurf` `cline` `roo` `opencode` `goose` `kiro` `workbuddy`，或 `all`。
内容一致时判为 `unchanged` 跳过；有差异且未加 `--force` 时报 `conflict`，不会静默覆盖。
各宿主目录、字段支持与调用语法见 `references/agent-compat.md`。

## 异常处理

| 现象 | 处理 |
| --- | --- |
| 退出码 2（参数校验） | 逐条修正 `error.messages` 后重试；不要绕过校验 |
| 退出码 3（文件系统） | 检查权限与路径；已创建项保留，修好后重跑（幂等补齐） |
| 退出码 4（verify 缺失） | 去掉 `--verify` 重跑一次 |
| `--force` 权限不足 | 不重试，报告需提权或改用新路径 |
| 任务创建失败（宿主工具） | 停止后续创建，报告已完成与失败项；不要删除已有任务 |
| 调度文件生成失败 | 报告路径与错误；不要手工写 cron 行替代 |
| runner 命令不存在 | 停下来问用户用哪个 CLI，不要猜测 |
| 同 cwd 疑似重复任务 | 询问用户，禁止自动删除或改名 |
| 模板缺失 / 占位符未替换 | 技能自身损坏，停止并提示重新安装 |

## 输出

`scaffold.py` 输出 UTF-8 JSON：`ok`、`mode`、`vault`、`structure`、`created_dirs`、`existing_dirs`、`created_files`、`skipped_files`、`backed_up`、`changed`、`automations`、`summary_lines`、`warnings`。

`schedule.py` 输出：`platform`、`tasks`，按平台附带 `crontab` / `commands` / `script` / `plists` / `automations` / `spec`，以及 `written`、`instructions`。

`install.py` 输出：每个目标的 `path` 与 `action`（installed / replaced / unchanged / conflict / self）。

## 示例

```
用户：用 obsidian-auto 在 D:/Obsidian WH/读书笔记 建个知识库，只要 sources，每天 8 点整理
→ scaffold.py --path "D:/Obsidian WH/读书笔记" --name "读书笔记" --domain "读书笔记"
   --profile minimal --daily-time 08:00 --create-parents
→ 宿主有自动化工具则建 2 个任务（每日 08:00 / 每周日 21:00），时间全部取自用户
→ 否则 schedule.py --platform auto --write，展示生成的 cron / 计划任务命令等用户确认
```

## 文件结构

```
obsidian-auto/
├── SKILL.md                    本说明
├── scripts/
│   ├── scaffold.py             幂等骨架生成器
│   ├── schedule.py             各宿主调度生成器（cron / schtasks / launchd / workbuddy / json）
│   ├── install.py              多宿主安装器
│   └── tasks.py                两个任务的共享定义（prompt / 时间）
├── assets/templates/           AGENTS.md、README.md、index.md、log.md 模板
└── references/
    ├── parameters.md           完整参数、退出码、幂等与对账规则
    └── agent-compat.md         各 agent 目录、字段与调用差异
```

## 注意事项

- `raw/` 永远只读：只创建目录，不读不写其中任何文件。
- 幂等是硬要求：不要为了「结果一致」删除或覆盖已有文件。
- 任务 prompt 内嵌仓库绝对路径，移动仓库后需重新执行本技能更新任务。
- 系统级调度必须先经用户确认；不要静默注册 cron / 计划任务 / launchd。
- 目标路径若位于个人目录（桌面、文档等），只做新增，不做删改。
