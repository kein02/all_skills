# 跨 Agent 兼容性参考

本技能遵循开放 Agent Skills 规范（`SKILL.md` + `scripts/` + `references/` + `assets/`），
除 `name` 与 `description` 外不依赖任何宿主专有字段，因此同一份目录可以原样投放给多个 agent。

> 目录与字段的支持情况会随客户端版本变化，以下是 2026 年公开约定，落地前建议以对应客户端文档复核。

## 1. 技能目录

| 宿主 | 个人级 | 项目级 | 显式调用 |
| --- | --- | --- | --- |
| WorkBuddy | `~/.workbuddy/skills/` | `.workbuddy/skills/` | 直接描述任务即可 |
| Claude Code | `~/.claude/skills/` | `.claude/skills/` | `/obsidian-auto` |
| Codex CLI | `~/.codex/skills/` | `.codex/skills/` | `$obsidian-auto` |
| Cursor | `~/.cursor/skills/` | `.cursor/skills/`（也认 `.agents/skills/`） | 描述触发，装完需重载窗口 |
| GitHub Copilot | `~/.copilot/skills/` | `.github/skills/` | 描述触发（匹配偏保守） |
| Gemini CLI | `~/.gemini/skills/` | `.gemini/skills/`（也认 `.agents/skills/`） | 描述触发 |
| Windsurf | `~/.codeium/windsurf/skills/` | `.windsurf/skills/` | 描述触发 |
| Cline | `~/.agents/skills/` | `.agents/skills/` | 描述触发 |
| Roo Code | `~/.roo/skills/` | `.roo/skills/` | 描述触发 |
| OpenCode | `~/.config/opencode/skills/` | `.opencode/skills/` | 描述触发 |
| Goose | `~/.config/goose/skills/` | `.goose/skills/` | 描述触发 |
| Kiro | `~/.kiro/skills/` | `.kiro/skills/` | 描述触发 |

`.agents/skills/` 是事实上的公共路径，Codex、Cursor、Copilot、Gemini、Cline 都会读，
想一次覆盖多数客户端时优先放这里。安装由 `scripts/install.py` 完成。

## 2. frontmatter 字段

| 字段 | 兼容性 | 本技能用法 |
| --- | --- | --- |
| `name` | 全部支持，必须与目录名一致 | `obsidian-auto` |
| `description` | 全部支持，触发完全依赖它 | 写明「做什么 + 何时用 + 触发词」 |
| `license` | 部分支持 | 未使用 |
| `compatibility` | 部分支持 | 声明 Python 与系统要求 |
| `metadata` | 部分支持 | 记录版本 |
| `agent_created` | WorkBuddy 专用，其他宿主忽略 | 保留，便于本机后续编辑 |
| `allowed-tools` / `context` / `hooks` | 仅个别宿主 | **不使用**，避免换宿主流失约束 |

结论：只保留 `name` / `description` / `compatibility` / `metadata`（+ WorkBuddy 的 `agent_created`），
其余一律不写，保证「拷过去就能用」。

## 3. 定时任务能力

| 宿主 | 内置调度 | 推荐落地方式 |
| --- | --- | --- |
| WorkBuddy | 有（automation 工具） | `--platform workbuddy`，由 Agent 调工具创建 |
| Claude Code | 无 | `--platform cron/schtasks/launchd`，runner 用 `claude -p` |
| Codex CLI | 无 | 同上，runner 用 `codex exec`（stdin 支持以官方文档为准） |
| Gemini CLI | 无 | 同上，runner 用 `gemini -p` |
| Cursor / Windsurf / Cline / Copilot | 无 | 同上，需本机装有对应 CLI 才能被调度器唤起 |
| 纯对话型 agent | 无 | 只建结构，`--platform json` 留档，需要时手动触发 |

所有非 WorkBuddy 场景都走 `scripts/schedule.py`：它生成 prompt 文件、包装脚本和调度文件，
由用户确认后再注册到系统（cron / 计划任务 / launchd 属于系统级改动，不要静默执行）。

## 4. 调用差异与坑

- **触发依赖 description**：描述含糊时各宿主都可能不加载；本技能描述已覆盖「新建知识库 / 搭结构 / 加定时任务」三类说法。
- **Cursor 需重载窗口**：装完技能不重载不会出现。
- **Copilot 触发保守**：提示词需贴近描述用词（如「用 obsidian-auto 建知识库」）。
- **Codex 用 `$name` 显式调用**：自动触发偶尔不稳，可用 `$obsidian-auto` 直接点名。
- **嵌套目录不被发现**：技能必须位于 `skills/<name>/SKILL.md` 一层，不能放在分类子目录里。
- **脚本执行权限**：类 Unix 上复制后需保证 `scripts/*.py` 可读、包装脚本 `chmod +x`（install.py 与 schedule.py 已处理）。
