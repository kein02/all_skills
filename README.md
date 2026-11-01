# all_skills

个人在开发学习过程中总结的 Agent skills 集合（适用于 ZCode、Claude Code 等支持 Agent Skills 标准的工具）。每个 skill 一个独立目录，把对应文件夹拷入 `~/.agents/skills/` 即可安装。

## 技能导引

| 技能 | 简介 |
|---|---|
| [readme-writer](readme-writer/README.md) | **README Writer**：为代码仓库自动生成"高星项目水准"的 README。基于对 11 个 100k+ star 项目（React、Vue、Ollama、nvm、HowToCook 等）与 4 份权威指南（Awesome README、Standard Readme、Make a README、GitHub 官方文档）的调研：自动判断项目类型（库 / CLI 工具 / Web 应用 / 框架 / 内容库 / 学术复现 / 插件），按类型套用对应的高星项目结构蓝图，遵守十条黄金原则写作，交付前过一遍自检清单。内置防编造护栏——README 中每个事实必须来自仓库实际内容。 |

→ 点技能名进入其详细说明（解决什么问题、安装、触发方式、工作流程、定制方法）；每个 skill 文件夹内 SKILL.md 为 Agent 读取的入口，README.md 为人类阅读的使用文档。

## 新增技能

保持「一个 skill 一个文件夹」的结构：

- 文件夹名 = skill 名（小写 kebab-case）
- 入口为 `SKILL.md`，YAML frontmatter 只需 `name` + `description`（description 写清"何时触发"，是自动触发的关键）
- 长内容放 `references/`（按需读取）、脚本放 `scripts/`、模板放 `assets/`
- 新增后在上方「技能导引」表格补一行
