# 项目类型识别与结构蓝图

来源：React、Vue、freeCodeCamp、TensorFlow、Oh My Zsh、Ollama、nvm、HowToCook、chinese-poetry、JavaGuide、996.ICU 的 README 实测调研。

## 第一步：识别信号表

| 类型 | 识别信号 | 参考项目 |
|---|---|---|
| 库 / SDK | 有包管理清单且准备发布（npm/PyPI/crates/Maven）；被 import 而非直接运行；无 UI、无 CLI 主入口 | React、Vue |
| CLI / 终端工具 | `bin` 字段 / console_scripts / main 函数解析 argv；用户在终端敲命令使用 | nvm、Ollama、Oh My Zsh |
| Web 应用 / 独立软件 | 有前端或 Docker/数据库配置；需启动服务或安装到设备；有 UI 资源 | freeCodeCamp |
| 框架 / 平台 | 提供脚手架或插件机制，用户在其上构建自己的项目；常有生态目录 | TensorFlow（平台型） |
| 内容库 / 知识库 / awesome-list | README 几乎无代码，主体是分类链接目录；或 `awesome-*`、笔记/教程库 | HowToCook、JavaGuide、chinese-poetry |
| 学术 / 算法复现 | 有论文引用、实验脚本、数据集下载说明、results/ 目录 | ML 论文仓库常见形态 |
| 插件 / 扩展 | 依赖某个宿主（vscode 扩展、浏览器扩展、zsh 插件、loader）；有 marketplace 清单 | Oh My Zsh 的插件 |

判断口诀：**用户拿到手第一件事是什么？** import 它 → 库；敲命令 → CLI；打开界面 → 应用；建新项目 → 框架；阅读 → 内容库；跑实验 → 学术；装进宿主 → 插件。

---

## 第二步：套对应的结构蓝图

### 库 / SDK（React 式，极简主义）

总长目标 ≤ 100 行。

1. 标题 + 徽章（版本 / 构建 / license）
2. 一句话定位 + 1~3 个**加粗**卖点（React 的写法：声明式、组件化、一次学习随处编写）
3. 一个最小示例代码块（10 秒见效果）
4. 一行安装命令（`npm install xxx` / `pip install xxx`）
5. 文档链接（外链 docs 站或 `docs/` 目录）
6. Contributing（附 good first issue 链接）
7. License（最后一节）

> 禁忌：不要在库里塞完整教程、API 全表、changelog。Vue 的 README 甚至零安装命令，一行链接指向官网。

### CLI / 终端工具（nvm / Ollama 式，README 内完成上手）

1. Logo（可用 SVG 支持明暗双模式）+ 徽章
2. 一句话定位
3. About 段落（2~4 行，说清解决什么问题）
4. Getting Started：前置要求（OS/版本兼容**表格**）→ 一行安装命令（curl/包管理器）→ 国内用户附镜像源提示
5. Usage：常用命令 + **真实终端输出**（如 `nvm install` 后展示 "Now using node v24"）
6. 配置说明：环境变量表或配置文件示例
7. Troubleshooting / FAQ：按平台或场景分节（Docker/CI/WSL 各一节）——这是降低 issue 数量的关键
8. 卸载方法
9. Contributing、License

### Web 应用 / 独立软件（freeCodeCamp 式，产品落地页）

1. 大 banner / logo
2. 一句话 + 特性 bullet
3. **在线 Demo 链接** + 截图/GIF（多张，展示核心界面）
4. 目录（内容长时）
5. 本地部署 / 自托管：依赖 → 安装 → 启动 → 默认端口/账号
6. 配置表：环境变量 / 配置项用**表格**
7. 技术栈与架构简介（细节外链 ARCHITECTURE.md 或 docs/）
8. Contributing、License、赞助

### 框架 / 平台

1. Logo + 一句话定位
2. 核心概念 ≤ 3 条
3. 脚手架快速开始（`npx create-xxx` 一行命令）
4. 生态目录：按场景分类列下游项目，每个一句话描述，结尾一句"想加入？提个 PR"（Ollama 手法，把增长机制写进文档）
5. 文档站链接、RFC/治理说明
6. Contributing（含行为准则）、License

### 内容库 / 知识库 / awesome-list（HowToCook / JavaGuide 式，README 即目录）

1. 标题 + 一句话定位
2. 在线阅读链接（若已部署站点）
3. **目录即正文**：分类标题 + 链接列表；条目多时用 ⭐"必看"标记控制阅读优先级
4. 如何贡献：添加条目的格式要求与校验方式
5. 衍生作品 / 致谢
6. License

> 无安装章节，除非提供本地部署（如 HowToCook 的两行 Docker 命令）。

### 学术 / 算法复现

1. 标题（论文方法名）+ 徽章（arXiv / PDF / 会议）
2. **架构图放最显眼位置**（摘要图）
3. TL;DR 一句话结论
4. Citation：BibTeX 代码块**放前部**（学术仓库最被复制的内容）
5. 环境复现：依赖安装 → 数据下载 → 训练/评估命令表（每个实验对应一行命令）
6. 预期结果表：与论文指标对照
7. License、致谢

### 插件 / 扩展

1. 标题 + 宿主兼容版本表
2. 一句话 + 效果截图/GIF
3. 安装：marketplace 链接 + 手动安装两种方式
4. 配置示例：settings.json 等真实片段
5. 命令 / 快捷键列表（表格）
6. 兼容性与已知问题（诚实声明）
7. Contributing、License
