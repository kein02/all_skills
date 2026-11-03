# obsidian-auto 参数与行为参考

三条命令：`scaffold.py`（建结构）、`schedule.py`（配调度）、`install.py`（装到各 agent）。

## 1. scaffold.py 参数

| 参数 | 必填 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `--path` | 是 | — | 仓库绝对路径。不能是磁盘根目录，不能是已存在的文件 |
| `--name` | 否 | 路径最后一段 | 仓库名称，用于 README 标题、目录树与任务命名 |
| `--domain` | 否 | `通用知识管理` | 主题名称，写入 AGENTS.md 开头 |
| `--material-desc` | 否 | `文章、论文、笔记` | `raw/` 里放什么，出现在目录树与 README |
| `--profile` | 否 | `standard` | `standard` = raw + wiki/{concepts,entities,sources}；`minimal` = raw + wiki/sources |
| `--concept-desc` | 否 | `按主题汇总的概念、方法与观点` | 覆盖 concepts 说明；minimal 下无效 |
| `--entity-desc` | 否 | `按对象汇总的工具、人物与平台信息` | 覆盖 entities 说明；minimal 下无效 |
| `--source-desc` | 否 | `每份原始资料一份摘要与出处` | 覆盖 sources 说明 |
| `--extra-category` | 否 | 空 | 追加分类，格式 `名称:说明`，可重复；名称限小写字母/数字/`-`/`_`，1–31 位 |
| `--automations` | 否 | `on` | `off` 时不输出任务计划 |
| `--daily-time` | **必填** | — | 每日整理时间（HH:MM），无默认值，用户不给就报错 |
| `--weekly-day` | 否 | `MO` | 每周健康检查星期：MO/TU/WE/TH/FR/SA/SU |
| `--weekly-time` | **必填** | — | 每周健康检查时间（HH:MM），无默认值 |
| `--date` | 否 | 今天 | log.md 首条记录日期 |
| `--dry-run` | 否 | 关 | 只输出计划，不落盘 |
| `--verify` | 否 | 关 | 只检查骨架，缺失时退出码 4 |
| `--force` | 否 | 关 | 覆盖四件套前备份为 `*.bak-YYYYmmdd-HHMMSS` |
| `--create-parents` | 否 | 关 | 父目录不存在时一并创建 |

## 2. schedule.py 参数

| 参数 | 默认 | 说明 |
| --- | --- | --- |
| `--vault` | 必填 | 已存在的知识库绝对路径（不存在直接报错） |
| `--name` | 目录名 | 任务名前缀 |
| `--categories` | `concepts,entities,sources` | 与库内实际分类保持一致 |
| `--platform` | `auto` | `workbuddy` / `cron` / `schtasks` / `launchd` / `json` / `auto`（按操作系统选） |
| `--runner` | `claude -p` | 触发任务的 CLI；需能从 stdin 读 prompt |
| `--daily-time` / `--weekly-time` | 必填 | 每日整理 / 每周健康检查的触发时间，不提供默认值 |
| `--weekly-day` | `MO` | 每周健康检查的星期 |
| `--out` | `<vault>/.obsidian-auto` | 生成物目录 |
| `--write` | 关 | 真正写盘；不加只输出内容供预览 |

各平台产物：

| platform | 产物 |
| --- | --- |
| `workbuddy` | `automations` 数组（name / prompt / rrule / cwds），由 Agent 调 `automation_update` |
| `cron` | `crontab.txt` + `bin/*.sh` + `tasks/*.md` + `log/` |
| `schtasks` | `install-schedule.ps1`（UTF-8 BOM）+ `bin/*.cmd` + `tasks/*.md` |
| `launchd` | `launchd/*.plist` + `bin/*.sh` + `tasks/*.md` |
| `json` | `tasks.json`（含 prompt 全文，可移植到任意调度系统） |

## 3. install.py 参数

| 参数 | 默认 | 说明 |
| --- | --- | --- |
| `--target` | `workbuddy` | `all` 或 `claude,codex,cursor,...` 逗号分隔 |
| `--scope` | `user` | `user`（个人级）或 `project`（项目级） |
| `--project` | — | `--scope project` 时的项目根目录 |
| `--force` | 关 | 覆盖已存在的同名技能（先改名备份为 `.bak-时间戳`） |
| `--dry-run` | 关 | 只报计划 |

动作取值：`installed`（新装）、`replaced`（覆盖并备份）、`unchanged`（内容一致跳过）、`conflict`（存在差异且未加 --force）、`self`（目标即源目录）。

## 4. 退出码

| 退出码 | 含义 | 处理建议 |
| --- | --- | --- |
| 0 | 成功（含幂等无变更） | 继续 |
| 2 | 参数校验失败 | 读 `error.messages` 修正后重试，不要落盘 |
| 3 | 文件系统错误 | 检查权限与路径；已写入部分保留，重跑即可 |
| 4 | `--verify` 发现缺失 | 去掉 `--verify` 重跑补齐 |

## 5. 结构模型

`standard`（默认）：

```
<vault>/
├── raw/
├── wiki/concepts/
├── wiki/entities/
├── wiki/sources/
├── AGENTS.md
├── index.md
├── log.md
└── README.md
```

`minimal`：只建 `raw/`、`wiki/sources/`。`--extra-category` 在标准分类之后追加目录，README 表格、目录树、AGENTS.md 说明段自动生成对应条目。

## 6. 幂等语义

| 情况 | 行为 |
| --- | --- |
| 目录已存在 | 计入 `existing_dirs`，不重建 |
| 基础文件已存在 | 计入 `skipped_files`，内容一字不改 |
| 已存在 + `--force` | 先备份 `*.bak-<时间戳>`，再覆盖 |
| 重复执行 | `changed=false`，输出「无变更，幂等」 |
| `raw/` 内有资料 | 完全不触碰 |
| `wiki/` 下有知识页 | 完全不触碰 |
| 同名同 cwd 的定时任务 | 参数一致则跳过，不一致则更新 |
| 重复安装到同一技能目录 | 内容一致判 `unchanged`，不重复拷贝 |

脚本只处理「骨架」，不搬运内容；重复执行不会产生重复日志条目。

## 7. 定时任务对账（宿主工具路径）

以 `name` 完全相等 + `cwds` 规范化后相等为匹配键：

| 现有任务状态 | 动作 |
| --- | --- |
| 同名同 cwd，rrule 与 prompt 一致 | 跳过 |
| 同名同 cwd，rrule 或 prompt 不同 | `mode=update`，带 `id` 更新差异字段 |
| 无同名任务，但同 cwd 有名称相近任务 | 停下询问用户，避免重复 |
| 同名任务在别的 cwd | 新建 |
| 完全不存在 | `mode=create` |

系统级调度路径（cron / schtasks / launchd）不自动注册：先生成、示出命令，用户确认后再执行。

## 8. 环境要求

- Python 3.8+，仅标准库，无需 pip。
- Windows 路径含空格时整段加引号；生成的 `.ps1` 为 UTF-8 BOM，避免中文路径乱码。
- 脚本只做本地文件操作，不联网、不调用 API。

## 9. 常见问题

**Q：已有 Obsidian 仓库想补结构？** 直接对现有路径执行，只补缺失项；`欢迎.md`、`.obsidian/` 不动，`欢迎.md` 是否删除单独征求用户同意。

**Q：报「父目录不存在」？** 加 `--create-parents`，或先建好父目录。

**Q：想改文案（如把「论文」换成「专利」）？** 用 `--material-desc`、`--domain` 等覆盖，不要改模板；模板是幂等基线。

**Q：换 agent 后定时任务怎么办？** 结构可复用，任务需在新宿主重建：有自动化工具走 `scaffold.py` 的 `automations`，没有则 `schedule.py` 生成系统级调度。

**Q：执行到一半失败？** 看 `created_*` 列表，已创建部分保留；修好后重跑（幂等），无需回滚。任务只建了一部分时报告已完成与失败项，不要删除已有任务。
