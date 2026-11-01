# 项目类型识别与结构蓝图（18 类）

来源：31 个高星仓库实测调研（React、Vue、axios、django、next.js、node、ripgrep、bat、yt-dlp、immich、localsend、transformers、whisper、sd-webui、nanoGPT、hello-algo、CS-Notes、developer-roadmap、awesome-selfhosted、superpowers、sqlmap、sherlock、Marlin、Mindustry、mathiasbynens/dotfiles、nvm、ollama 等）。

## 判断流程：两问口诀

1. **读者拿到手第一件事是什么？** → 决定类型
2. **README 要回答什么问题？** → 决定角色与篇幅

| 角色 | 回答的问题 | 典型篇幅 |
|---|---|---|
| 自足型（库） | 怎么装、怎么用、API 随查 | 100 行~2800 行 |
| 入口型（框架） | 适不适合我、该去哪学 | 50~150 行 |
| 手册型（CLI/AI 应用/插件） | 怎么装、怎么配、出问题怎么办 | 中长 |
| 枢纽型（self-hosted） | 看效果、找部署入口 | 极短 |
| 目录型（内容库/教程） | 从哪开始读 | 目录为主 |
| 索引型（awesome/路线图） | 可信的检索 | 超长 |
| 治理型（运行时） | 怎么获取、校验、参与 | 中长 |
| 名片型（profile） | 30 秒认识你 | 短 |

## 识别信号表

| 类型 | 识别信号 | 代表仓库 |
|---|---|---|
| 库 / SDK | 包管理清单且准备发布；被 import；无 UI 无主入口 | axios、React |
| 框架 / 平台 | 提供脚手架/插件机制，用户在其上构建项目 | django、next.js、TensorFlow |
| 语言运行时 | 实现/分发一门语言或执行环境；有 LTS/版本发布体系 | node |
| CLI 工具 | bin 字段 / console_scripts / argv 解析 | ripgrep、bat、yt-dlp |
| Self-hosted 应用 | Docker/数据库配置，需自部署成服务 | immich |
| 桌面 / 移动应用 | 面向最终用户的安装包（exe/dmg/APK/商店） | localsend |
| AI 模型 / AI 库 | 模型权重、推理/训练库、模型规模表 | transformers、whisper |
| AI 应用 | 带 UI 的 AI 工具，用户是玩家/创作者 | sd-webui |
| 论文复现 / 学术 | 论文引用、实验脚本、数据集下载说明 | nanoGPT |
| 知识库 / 教程 | 主体是章节化内容，常配在线站点 | hello-algo、CS-Notes |
| 学习路线图 | 路径图/技能清单，常配交互网站 | developer-roadmap |
| awesome 聚合 | 大量第三方条目按分类罗列 | awesome-selfhosted |
| 插件 / Agent Skill | 依赖宿主；marketplace 清单或 SKILL.md 入口 | superpowers |
| 安全工具 | 攻击/检测能力，需授权使用 | sqlmap、sherlock |
| 硬件 / 嵌入式 | 固件/驱动，面向板卡矩阵 | Marlin |
| 游戏 | 可玩的成品或引擎 | Mindustry |
| dotfiles / 配置 | 个人环境配置脚本集合 | mathiasbynens/dotfiles |
| Profile 主页 | `<user>/<user>` 仓库，纯展示 | 各类 stats 卡用户 |

速记：import→库；建新项目→框架；选版本装环境→运行时；敲命令→CLI；部署→self-hosted；下载安装→应用；跑模型→AI；复现数字→学术；阅读→内容库；点路径→路线图；检索→awesome；装进宿主→插件；授权测试→安全；刷机→硬件；玩→游戏；抄配置→dotfiles；认识你→profile。

---

## 一、代码与运行时

### 1. 库 / SDK（自足型）

1. 标题 + 徽章（版本 / 构建 / **安装体积** / 下载量）
2. 一句话定位 + 1~3 个加粗卖点
3. 一个最小示例代码块（紧贴安装节之后）
4. 多包管理器安装（npm/yarn/pnpm/CDN 各一行）+ semver/TS 支持声明
5. API 参考（大库可内嵌，**必须配锚点目录**；小库外链 docs）
6. 浏览器/平台兼容（logo 表格）
7. Contributing、License

> 篇幅与库复杂度成反比：axios 2800 行内嵌全 API（有目录兜底），React/Vue 极简全外链。赞助位别前置（推迟首屏有效信息）。

### 2. 框架 / 平台（入口型，50~150 行）

1. Logo + 定位宣言（express："Fast, unopinionated, minimalist"）
2. 特性列表 + 最小示例
3. 文档 / 教程 / 社区 全外链——django 连安装命令都不放，直接指向 docs/intro
4. 安全披露：写明漏洞**不要开公开 issue**，给 SECURITY.md 链接
5. Contributing（含行为准则）、License

> monorepo 根 README 易缺指引：next.js 用一行指针指向真身 `packages/next/README.md`。使用者/贡献者用外链分流，别都塞进 README。

### 3. 语言运行时（治理型）

1. 发布类型与生命周期（Alpha/Current/LTS/Nightly 语义 + 版本节奏）
2. 下载渠道 + **二进制校验（gpg 命令级细节）**
3. 构建指引（细节外链 BUILDING.md）
4. 治理模型（外链 GOVERNANCE.md）+ 团队名单（`<details>` 折叠 emeriti）
5. License

> 不写"XX 是什么"营销话术与使用教程（推官网）。注意：名单格式可能被内部脚本依赖，改前看源码注释。

---

## 二、工具与应用

### 4. CLI 工具（手册型）

1. Logo + 徽章
2. 一句话定位，**写清与被替代工具的关系**（ripgrep："grep 的更快替代"）
3. 效果证明：bench 表（**必须标测量环境**）或截图，紧跟所证明的特性
4. 双向诚实：Why use / Why **not** use
5. 安装：**按渠道分小节**（brew/apt/choco/cargo 各一条可复制命令，bat 用 `On Ubuntu` 标题）
6. Usage：常用命令 + 真实终端输出 + 管道/别名真实用法
7. 配置说明 + Troubleshooting（按平台/场景分节）+ 卸载
8. Contributing、License

> 选项多了外置：yt-dlp 180KB 手册靠标记自动生成，不是手写。

### 5. Self-hosted 应用（枢纽型，越短越好）

1. for-the-badge 徽章 + 居中 logo + tagline + **大截图**
2. 多语言切换行（链接行，不翻译正文）
3. Demo（含体验账号）
4. 功能矩阵表（**按端拆列**：Mobile/Web）
5. 显著的部署文档链接 + 安全警示（如 3-2-1 备份，用 `> [!IMPORTANT]`）
6. contrib.rocks + Repobeats 活跃度图（营造"活的"信任）
7. License

> **完整安装步骤一律沉淀 docs 站**——Docker compose 全文进 README 必过期。immich 正文仅 5KB。

### 6. 桌面 / 移动应用（下载页型）

1. 徽章 + 导航行（官网/Discord）+ About 一段
2. 双端截图并排（限高）
3. **下载矩阵（平台×渠道，全部直达链接）** + 最低系统版本兼容表
4. Setup / Troubleshooting 表（症状×平台×解法）——需要权限/防火墙的应用必写
5. 无自动更新要明说；分平台 Building（细节）
6. Contributing、License

> 捐赠走 FUNDING.yml，不混正文。代码级细节不写（读者不看源码）。

---

## 三、AI 与学术

### 7. AI 模型 / AI 库（文档+选型表型）

1. `<picture>` 明暗 logo + 徽章墙 + 多语言行
2. `[Blog][Paper][Colab]` 链接行
3. 安装（**含 Python/PyTorch 版本下限**；依赖坑逐平台给命令，如 ffmpeg 五种包管理器）
4. 最小可运行示例**附真实输出**；`<details>` 按模态折叠更多示例
5. **模型规模表（参数量 × 显存 × 相对速度）**，性能必须标测量条件
6. 模型选型坑写进正文（`> [!NOTE]`：如 turbo 不支持翻译）；双向陈述 Why/When not use
7. Citation / BibTeX 收尾

### 8. AI 应用（装机手册型）

1. H1 + 一句话 + **截图直接开场**
2. 功能大清单（求全，二级 bullet + 内联语法示例）
3. 安装按**硬件分链**（NVIDIA/AMD/Intel）再分平台逐步写
4. **硬版本约束写死正文**（"Python 3.10.6，更新版不支持 torch"）；版本 workaround 必须内联
5. 第一层"装不上"排障留 README，其余移交 wiki
6. Credits 长列表维护社区关系

### 9. 论文复现 / 学术（实验手册型）

1. 标题 + arXiv/PDF/会议徽章 + 架构图放最显眼
2. **开头量化承诺**（nanoGPT："8×A100 四天复现 124M"）
3. Quick start **按硬件分支**（"I have a GPU" / "I only have a macbook"）给完整命令 + 预期 loss 输出
4. baselines 表对齐论文数字；贴真实生成样本（含失败样本+自嘲）
5. 复现自己论文 → Citation 放前部；复现别人论文 → 用 **todos 声明未做之事** + troubleshooting
6. License、致谢

> 实验性依赖给关闭开关写进 troubleshooting；人设化口语是风格资产。

---

## 四、内容与聚合

### 10. 知识库 / 教程（书的封面 + 目录型）

1. 居中 header + 动画/GIF + CTA 大按钮（导流在线站点/PDF）
2. ≤3 条价值点 + **权威推荐语**（清华教授/李沐）
3. 多语言切换行（**目录+一行切换**，别靠分支）
4. 分区目录即正文：emoji 分区 + 🔥高频标记 + ⭐必看
5. 按人群入口（按天学习路线）
6. 如何贡献（条目格式与校验）、License

> 知识内容绝不进 README；站点与 README 双头维护必漂移；在线入口给静态兜底。

### 11. 学习路线图（索引引流型）

1. Logo + badge 按钮当站内导航
2. 完整路线清单（**正式版/新手版两级并排**，防 90 条吓退读者），条目只留名字
3. **仓库结构与自动同步机制**（PR 改哪里、怎么同步到网站）
4. 贡献方式 + contrib.rocks + 分享徽章

> 真产品是交互网站，README=索引页+引流；双载体必须写明分工，否则 PR 改错地方。

### 12. awesome 聚合（数据库型）

1. 头部三徽章立信用：awesome 官标 + **死链 CI** + **失维 CI**
2. 收录范围声明（如仅自由软件，非自由另页）
3. TOC → `##`大类/`###`子类 → 每类"back to top + 一句定义 + Related"三件套
4. 硬性统一条目格式：名 + 一句话描述 + Demo/Source Code + 协议 + 技术栈内联徽章 + ⚠反特性标记
5. 不收裸链接；按字母序不按热度；附 SPDX 协议速查表
6. 收录标准（contributing）、License

> 规模一大**必须自动化**（data 仓库+CI 查死链）；条目质量 > 排版粉饰——这是 awesome 系的生命线。

---

## 五、垂直场景

### 13. 插件 / Agent Skill（安装手册型）

1. 标题 + 宿主兼容表 / 效果截图
2. 开头一句管理预期（**多宿主需分别安装**）
3. 安装**每宿主一小节**（目录锚点直达）：官方 marketplace 一行命令 → fallback → 通用 CLI 兜底（`npx skills add owner/repo -s <skill>`）→ 手动 clone+拷贝
4. `> [!IMPORTANT]`：装完需新开会话/重启宿主生效
5. **验证**：给一句能触发该 skill 的验证 prompt
6. **更新 = 重跑同一条安装命令**（旧版自动备份）
7. 配置示例、命令/快捷键表、已知问题
8. Contributing、License

> badge 即按钮（skills.sh 徽章链到安装页）。完整模板见 `install-patterns.md`。

### 14. 安全工具（合规+手册型）

1. 徽章 → 一句话攻击能力边界
2. **合规声明（仅授权测试/教育用途）放首屏或 License 前**
3. Demo GIF → 安装表（pipx/docker/包管理器）
4. 最小用法 + 完整 `--help` 输出 + 手册/FAQ 外链
5. 第三方包损坏用 `> [!WARNING]` 显式标
6. contrib.rocks、Star History、License

> 不写攻击教程与绕过细节（留 wiki）；不写营销文案。

### 15. 硬件 / 嵌入式（兼容矩阵型）

1. 居中大 logo + 徽章墙 + 翻译表
2. **分支状态警示加粗**（Marlin："Bugfix Branch **Not for production use!**"）——变砖风险与版本混乱是头号坑
3. 配置获取方式（常是独立 Configurations 仓库）
4. 构建工具链优先级（VSCode+PlatformIO 优先，Arduino 次之）
5. 平台支持矩阵（Platform|MCU|Example Boards）
6. 社区支持渠道与 Issue 分工、贡献规范（分支模型/build tests）
7. **GPL 对厂商的义务说明**（License 段讲义务，不只贴名字）

> 刷写步骤不放 README，全在官网文档。

### 16. 游戏（双受众分流型）

1. 仓库内资产做 logo + 类型定位一句话
2. 外链三件套（Wiki/Trello/API 文档）
3. **构建版本精确约束**（"JDK 17，Other versions will not work" 加粗）
4. FAQ 式排障（chmod、生成代码在哪）+ 预期管理（构建要等几分钟、产物路径、生成代码不可手改）
5. 给不想编译的人留 bleeding-edge builds 链接；功能请求分流独立仓库
6. 玩家 → 商店徽章表格收尾；玩法介绍放 wiki/商店页

### 17. dotfiles / 配置（警示+脚本型，零徽章零动画）

1. 截图开路
2. **Warning 放安装最前**：fork 后先审查代码，Use at your own risk
3. 一条命令安装/更新（Git+bootstrap 脚本 + Git-free 两种）
4. 自定义扩展点（`~/.extra`）+ 敏感信息隔离示例（git 凭据不入库）
5. Feedback/Author/致谢

> 读者诉求是"安全地变成我自己的"——不逐文件解释 alias，短小克制。

### 18. Profile 个人主页（名片型）

常见元素按需组合：打招呼（角色+地域+emoji wave）→ 社交徽章墙/simple-icons 图标行 → 访客计数 → 🔭正在做/🌱在学/💬联系我 → 技术栈图标墙 → github-readme-stats 统计卡 → 代码块式自我介绍 → 结尾署名。

> 重度依赖第三方服务（统计卡/计数器）失效是常态；**克制型（纯文本三行+外链）反而更显专业**。

---

## 混合型处理

既是库又带 CLI（如 ollama）、既有应用又做 SaaS（如 immich）——按**用户的主要使用方式**归类定主蓝图，合并次要身份的 1~2 个关键节（如库蓝图 + CLI 的安装小节）。两问口诀里"第一件事"以多数读者为准。
