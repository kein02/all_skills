# readme-writer

[English](README.en.md) | 简体中文

一个 Agent Skill：对 Agent 说一句话，它就为你的代码仓库自动写出"高星项目水准"的 README——先判断项目类型，再按对应的成熟结构写作，交付前自动过一遍质检清单。

![type](https://img.shields.io/badge/type-agent--skill-blue) ![scope](https://img.shields.io/badge/scope-personal-green)

## 它解决什么问题

大多数人写的 README 有三种死法：文字墙（没人读）、看不懂（说不清项目是什么）、跑不起来（没有可复制的安装命令）。

本 skill 的方法论来自一次实测调研：**11 个 100k+ star 项目**（React、Vue、freeCodeCamp、TensorFlow、Oh My Zsh、Ollama、nvm、HowToCook、chinese-poetry、JavaGuide、996.ICU）+ **4 份权威指南**（Awesome README、Standard Readme、Make a README、GitHub 官方文档），提炼成两条心法与一套可执行工作流：

> README 是路由器，不是文档；前三屏决定生死（定位句 + 安装命令 + 演示）。

## 安装

不同 Agent 工具安装方式不同；如在多个工具中使用，请分别安装。以下任选一种：

**一键脚本**（拷入 `~/.agents/skills/`，旧版自动备份）：

```bash
curl -fsSL https://raw.githubusercontent.com/kein02/all_skills/main/install.sh | bash -s -- readme-writer
```

**社区 CLI**（skills.sh，支持多种 agent 工具）：

```bash
npx skills add kein02/all_skills -s readme-writer
```

**手动**（无其他依赖，项目级安装也用这种：放进 `<项目>/.agents/skills/` 即可）：

```bash
git clone --depth 1 https://github.com/kein02/all_skills
mkdir -p ~/.agents/skills && cp -r all_skills/readme-writer ~/.agents/skills/
```

> [!IMPORTANT]
> 安装后需**新开一个会话**才生效（skills 目录在会话启动时扫描），当前会话可用 `/readme-writer` 强制调用。

**验证**：新会话里说一句"帮我给这个项目写个 README"，能自动进入工作流即安装成功。

**更新**：重跑同一条安装命令（旧版自动备份为 `readme-writer.bak.<时间戳>`）。

## 使用方法

**自动触发**——包含以下意思的说法会自动激活：

- "帮我给这个项目写个 README"
- "我的 README 没人看得懂，帮我重写"
- "我要开源这个项目，准备一下文档"

**手动调用**——；如在部分Agent中输入 `/readme-writer`（自动触发没反应时用它兜底）。

## 工作流程

触发后 Agent 会走这 6 步：

| 步骤 | 做什么 | 关键规则 |
|---|---|---|
| 1. 侦察仓库 | 读 package.json / pyproject.toml / tests / examples / CI 配置，建立"事实清单" | 每个事实必须有出处，**禁止编造** |
| 2. 判断类型 | 按两问口诀归入 18 类之一并定位角色（见下表） | 混合型按用户主要使用方式归类 |
| 3. 套结构蓝图 | 按类型的成熟章节顺序定大纲 | 安装永远靠前，License 永远收尾 |
| 4. 写作 | 按十条黄金原则成文 | 没证据的信息留 `<!-- TODO -->`，不瞎编 star 数/用户评价 |
| 5. 自检 | 逐项过质检清单 | 相对链接、徽章 ≤5、渲染 <500 KiB、无文字墙 |
| 6. 交付 | 写入 README.md 并报告 | 说明判断的类型与理由，列出待你补充的 TODO |

### 支持的 18 种项目类型

两问口诀：① **读者拿到手第一件事是什么？**（定类型）② **README 要回答什么问题？**（定角色与篇幅——自足/入口/手册/枢纽/目录/索引/治理/名片）

| 分组 | 类型 | 拿到手第一件事 | 代表高星项目 |
|---|---|---|---|
| 代码与运行时 | 库 / SDK | import 它 | axios、React |
| 代码与运行时 | 框架 / 平台 | 建新项目 | django、TensorFlow |
| 代码与运行时 | 语言运行时 | 选版本装环境 | node |
| 工具与应用 | CLI 工具 | 敲命令 | ripgrep、yt-dlp |
| 工具与应用 | Self-hosted 应用 | 部署它 | immich |
| 工具与应用 | 桌面/移动应用 | 下载安装 | localsend |
| AI 与学术 | AI 模型 / AI 库 | 跑模型 | transformers、whisper |
| AI 与学术 | AI 应用 | 我显卡能不能跑 | sd-webui |
| AI 与学术 | 论文复现 | 复现到论文数字 | nanoGPT |
| 内容与聚合 | 知识库 / 教程 | 开始阅读 | hello-algo、HowToCook |
| 内容与聚合 | 学习路线图 | 点开路径 | developer-roadmap |
| 内容与聚合 | awesome 聚合 | 检索找工具 | awesome-selfhosted |
| 垂直场景 | 插件 / Agent Skill | 装进宿主 | superpowers |
| 垂直场景 | 安全工具 | 授权测试 | sqlmap、sherlock |
| 垂直场景 | 硬件 / 嵌入式 | 刷机 | Marlin |
| 垂直场景 | 游戏 | 玩或编译 | Mindustry |
| 垂直场景 | dotfiles / 配置 | 抄走自用 | mathiasbynens/dotfiles |
| 垂直场景 | Profile 主页 | 认识你 | github-readme-stats 用户 |

每种类型的完整结构蓝图（章节顺序、排版手法、注意事项）见 `references/project-types.md`；跨类型五条铁律（角色决定篇幅、越成熟越短、价值证明前置、警示内联、规模大上自动化）见 `references/principles.md`。均为按需加载，不占日常上下文。

## 文件结构

```
readme-writer/
├── SKILL.md                      # 入口：触发条件 + 6 步工作流（约 100 行）
└── references/                   # 按需加载，不占日常上下文
    ├── project-types.md          # 类型识别信号表 + 7 套结构蓝图
    ├── principles.md             # 板块清单、十条原则、反模式、徽章速查、模板骨架
    └── install-patterns.md       # 安装/分发板块写法速查（零摩擦七条 + 生态命令表）
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
