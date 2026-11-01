# readme-writer

一个 Agent Skill：对 Agent 说一句话，它就为你的代码仓库自动写出"高星项目水准"的 README——先判断项目类型，再按对应的成熟结构写作，交付前自动过一遍质检清单。

![type](https://img.shields.io/badge/type-agent--skill-blue) ![scope](https://img.shields.io/badge/scope-personal-green)

## 它解决什么问题

大多数人写的 README 有三种死法：文字墙（没人读）、看不懂（说不清项目是什么）、跑不起来（没有可复制的安装命令）。

本 skill 的方法论来自一次实测调研：**11 个 100k+ star 项目**（React、Vue、freeCodeCamp、TensorFlow、Oh My Zsh、Ollama、nvm、HowToCook、chinese-poetry、JavaGuide、996.ICU）+ **4 份权威指南**（Awesome README、Standard Readme、Make a README、GitHub 官方文档），提炼成两条心法与一套可执行工作流：

> README 是路由器，不是文档；前三屏决定生死（定位句 + 安装命令 + 演示）。

## 安装

把 `readme-writer/` 整个文件夹拷入 skills 目录即可，无其他依赖：

| 范围 | 路径 | 生效范围 |
|---|---|---|
| 个人级（推荐） | `~/.agents/skills/readme-writer/` | 所有项目可用 |
| 项目级 | `<项目>/.agents/skills/readme-writer/` | 仅当前项目 |

适用于 ZCode、Claude Code 等支持 Agent Skills 标准（`SKILL.md` + YAML frontmatter）的工具。安装后新开会话生效。

## 使用方法

**自动触发**——包含以下意思的说法会自动激活：

- "帮我给这个项目写个 README"
- "我的 README 没人看得懂，帮我重写"
- "我要开源这个项目，准备一下文档"

**手动调用**——在 ZCode 中输入 `/readme-writer`（自动触发没反应时用它兜底）。

## 工作流程

触发后 Agent 会走这 6 步：

| 步骤 | 做什么 | 关键规则 |
|---|---|---|
| 1. 侦察仓库 | 读 package.json / pyproject.toml / tests / examples / CI 配置，建立"事实清单" | 每个事实必须有出处，**禁止编造** |
| 2. 判断类型 | 按识别口诀归入 7 类之一（见下表） | 混合型按用户主要使用方式归类 |
| 3. 套结构蓝图 | 按类型的成熟章节顺序定大纲 | 安装永远靠前，License 永远收尾 |
| 4. 写作 | 按十条黄金原则成文 | 没证据的信息留 `<!-- TODO -->`，不瞎编 star 数/用户评价 |
| 5. 自检 | 逐项过质检清单 | 相对链接、徽章 ≤5、渲染 <500 KiB、无文字墙 |
| 6. 交付 | 写入 README.md 并报告 | 说明判断的类型与理由，列出待你补充的 TODO |

### 支持的 7 种项目类型

判断口诀：**用户拿到手第一件事是什么？**

| 类型 | 拿到手第一件事 | 结构风格 | 参考项目 |
|---|---|---|---|
| 库 / SDK | import 它 | 极简，≤100 行，学习内容全外链 | React、Vue |
| CLI 工具 | 敲命令 | 完整安装 + 真实终端输出 + Troubleshooting | nvm、Ollama |
| Web 应用 | 打开界面 | 产品落地页：Demo + 截图 + 部署步骤 | freeCodeCamp |
| 框架 / 平台 | 建新项目 | 脚手架一行命令 + 生态目录 | TensorFlow |
| 内容库 | 阅读 | README 即目录 + ⭐必看标记 | HowToCook、JavaGuide |
| 学术复现 | 跑实验 | 复现命令表 + BibTeX 放前部 | ML 论文仓库 |
| 插件 / 扩展 | 装进宿主 | 宿主兼容表 + 配置示例 | OMZ 插件 |

## 文件结构

```
readme-writer/
├── SKILL.md                      # 入口：触发条件 + 6 步工作流（约 100 行）
└── references/                   # 按需加载，不占日常上下文
    ├── project-types.md          # 类型识别信号表 + 7 套结构蓝图
    └── principles.md             # 板块清单、十条原则、反模式、徽章速查、模板骨架
```

## 定制

- 想改某类项目的章节顺序 → 编辑 `references/project-types.md` 中对应蓝图
- 想调整写作原则或反模式 → 编辑 `references/principles.md`
- 想改触发时机 → 编辑 `SKILL.md` 的 `description` 字段（它是自动触发的唯一依据）

## 已知边界

- 语言跟随当前对话；检测到国际受众信号（英文 README/issue）会先问一句"中文 / 英文 / 双语"再动笔
- 截图、GIF、打赏码这类仓库里没有的素材不会伪造，会以 TODO 清单形式列出请你补
- 已有 README 时会先读再改，保留你添加的链接与徽章；若项目不在 git 管理下，覆盖前会先确认
- 为 CLI 生成"真实终端输出"时只运行安全只读命令

## 反馈与改进

用出问题（判型错误、结构不合理、触发不灵）直接在本仓库提 issue，或在 issue 里贴上当时的仓库与产出，便于迭代蓝图。
