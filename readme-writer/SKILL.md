---
name: readme-writer
description: 为代码仓库生成或重写高质量 README，自动判断项目类型（库/工具/应用/AI/内容库/插件等 18 类）并套用对应的高星项目结构与角色定位。基于对 31 个高星仓库（React、Vue、axios、immich、yt-dlp、transformers、nanoGPT、hello-algo、superpowers、Marlin 等）与 4 份权威指南（Awesome README、Standard Readme、Make a README、GitHub 官方文档）的调研。当用户想给项目写 README、生成说明文档、优化或重写现有 README、初始化 GitHub 仓库、准备开源发布，或抱怨"没人明白我的项目是干嘛的"时使用。触发词：写 readme、生成 README、README 怎么写、项目文档、仓库说明、开源准备。Use when the user asks to write, generate, improve, or rewrite a README, or prepare a repo for open-source release — even if they don't say "README" explicitly, as long as they want their GitHub project to present itself better.
---

# README Writer

为任意代码仓库写出"高星项目水准"的 README。

方法论来源：对 11 个 100k+ star 项目（React、Vue、freeCodeCamp、TensorFlow、Oh My Zsh、Ollama、nvm、HowToCook、chinese-poetry、JavaGuide、996.ICU）和 4 份权威指南（Awesome README、Standard Readme、Make a README、GitHub 官方文档）的调研。

## 两个心法（写之前先记住）

1. **README 是路由器，不是文档**：只保留"上手所需"，深入内容外链 docs/wiki。README 篇幅与项目复杂度成反比——库类越短越好。
2. **前三屏决定生死**：访客流失发生在前 10 秒。黄金三件套 = logo/标题 + 一句话定位 + 一个可复制的安装命令。

## 工作流程

### 第 1 步：侦察仓库

快速建立"事实清单"——README 里每个事实都必须有出处，**禁止编造**。

- 清单文件：`package.json` / `pyproject.toml` / `setup.py` / `Cargo.toml` / `go.mod` / `pom.xml` / `requirements.txt` → 项目名、描述、依赖、scripts、版本、license 字段
- 入口与用法：main 文件、CLI 参数解析、`examples/`、`tests/`（测试里的调用方式就是真实用法）
- 生态信号：LICENSE 文件、`.github/workflows/`（CI 能力）、`docs/`、CHANGELOG、CONTRIBUTING、docker-compose、截图资源
- 已有 README.md（若有）：**先读**。保留用户添加的链接、徽章、联系方式、打赏信息，改进结构而不是清空重来。
- 分发渠道信号：发布到哪个 registry（npm/PyPI/crates…）、是否走 plugin/marketplace 机制（`.claude-plugin/`、`SKILL.md` 布局）、有无 install 脚本或预编译 releases——**安装节的写法必须与实际分发方式一致，没有发行渠道就先如实给 clone+构建路径**

### 第 2 步：判断项目类型

读 `references/project-types.md` 的识别信号表（18 类），用两问口诀定位：

1. **读者拿到手第一件事是什么？** → 决定类型（import→库；敲命令→CLI；部署→self-hosted；下载安装→应用；跑模型→AI；阅读→内容库；检索→awesome；装进宿主→插件；刷机→硬件……）
2. **README 要回答什么问题？** → 决定角色与篇幅（自足/入口/手册/枢纽/目录/索引/治理/名片）

完整清单：库/SDK、框架/平台、语言运行时、CLI 工具、Self-hosted 应用、桌面/移动应用、AI 模型与库、AI 应用、论文复现、知识库/教程、学习路线图、awesome 聚合、插件/Agent Skill、安全工具、硬件/嵌入式、游戏、dotfiles/配置、Profile 主页。

混合型项目（如"既是库又带 CLI"）按用户的主要使用方式归类，结构可合并两型要点。在报告里用一两句话说明判断依据。

### 第 3 步：按类型套结构

在 `references/project-types.md` 中找到该类型的章节蓝图，确定大纲。铁律：

- 安装永远靠前，贡献与 License 永远收尾（License 必须是最后一节）
- 安装节永远**一条可复制命令**首选；多平台/多宿主分区呈现，一个代码块只含一种环境；装完紧跟验证方法；更新方式有交代（模式速查见 `references/install-patterns.md`）
- 内容只保留"上手所需"，其余外链或 `<details>` 折叠

### 第 4 步：写作

读 `references/principles.md`，遵守十条黄金原则与反模式清单。硬性要求：

- 每个事实来自第 1 步清单。star 数、用户量、评价语录、打赏方式等**没有证据就不写**，用 `<!-- TODO: ... -->` 占位并在交付时提醒用户补充
- 安装/使用命令必须是从仓库推断出的**真实命令**，代码块可直接复制
- 示例附预期输出：从 tests/examples 推断；CLI 工具可以在本地实际运行命令捕获真实输出（只运行安全只读命令）
- 语言默认跟随用户当前对话语言；若仓库信号显示国际受众（现有英文 README、英文 issue），先一句话确认"中文 / 英文 / 双语"再动笔。确定双语后按 `references/principles.md` 的多语言支持规范落地：翻译放兄弟文件（README.en.md），标题下放双向切换行，结构性改动同步所有语言版本

### 第 5 步：自检

交付前逐项过：

- [ ] 前 3 屏齐全：定位句 + 安装命令 + 演示
- [ ] 安装节：一条可复制命令、与实际分发渠道一致、附验证方法；工具/插件类有更新交代
- [ ] 无文字墙：bullet、表格、代码块调节奏
- [ ] 仓库内链接全部是相对路径（fork/clone 后不断链）
- [ ] License 是最后一节，且与 LICENSE 文件一致
- [ ] 徽章 ≤5 个，全部有信息量（版本/构建/license 即可）
- [ ] 渲染体积 < 500 KiB（GitHub 硬限制，超出会被截断）
- [ ] 长内容已外链或 `<details>` 折叠

### 第 6 步：交付

1. 报告判断的项目类型与理由
2. 写入项目根目录 `README.md`。若已有 README 且项目**不在 git 管理下**，先向用户确认再覆盖
3. 列出待用户补充的 TODO 清单（截图、demo 链接、赞助方式等）

## 常见用法

- "帮我给这个项目写个 README"
- "我的 README 没人看得懂，重写一下"
- "我要开源这个项目，准备一下文档"
