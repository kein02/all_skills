# 安装 / 分发板块写法速查

来源：obra/superpowers（16 宿主安装手册）、anthropics/skills、starship、uv、gh cli、fzf 的安装节实测调研。

## 零摩擦安装七条

1. **一条可复制命令永远首选**，表格和其余渠道都是"alternatively"。渠道再多，第一条永远是那一行。
2. **按平台/宿主分区，一个代码块只含一种环境**（uv 用块首注释 `# On macOS and Linux.`，starship 用 `<details>` 折叠 + 平台表格，superpowers 每宿主一小节 + 目录锚点直达）。
3. **装完紧跟"接线"第二步**：安装 ≠ 可用（改 rc 文件、开新会话、执行 init）。用 GitHub 告警语法 `> [!IMPORTANT]` 承担这类提醒，不要埋在散文里。
4. **立即可验证**：跑一个最小示例（fzf）、开新终端看效果（starship）、对 Agent 说一句能触发功能的 prompt（superpowers："send 'Let's make a react todo list' — a working install auto-triggers brainstorming"）。
5. **更新方式有交代**：`uv self update`、fzf 按安装方式分列的 Upgrading 节、或 superpowers 的"重跑安装命令即更新"。
6. **prebuilt 二进制始终兜底**：releases 链接放最后；需要安全背书时给校验方式（gh 的 `gh at verify` / cosign）。
7. **渠道多时下沉**：README 只留主渠道，长尾渠道外链 docs 子页（gh 的 install_*.md 模式），主文件保持短。

## 生态速查表（安装命令必须与实际分发渠道一致）

| 分发渠道 | 标准一键命令 |
|---|---|
| Agent Skill（社区 CLI，事实标准） | `npx skills add <owner>/<repo> -s <skill名>`（skills.sh；anthropics 官方仓库也挂其徽章） |
| Claude Code 插件 | `/plugin marketplace add <owner>/<repo>` → `/plugin install <name>@<marketplace>` |
| 通用脚本 | macOS/Linux `curl -fsSL <install.sh> \| bash`；Windows `irm <url> \| iex`（各给独立代码块） |
| git 仓库（无发行渠道） | `git clone --depth 1 <url>` + **具体的**拷贝/构建命令——只说 clone 后"自行配置"等于没写 |
| npm 包 | `npm i -g <pkg>`；一次性运行 `npx <pkg>` |
| pip | `pip install <pkg>`；推荐隔离安装 `pipx install` / `uv tool install` |
| cargo / go / brew | `cargo install <pkg>` / `go install ...@<ver>` / `brew install <pkg>` |
| 预编译二进制 | releases 页链接 + 校验方式 |
| 编辑器/浏览器扩展 | marketplace 直链按钮 |

## Agent Skill 安装节模板（superpowers 式）

```markdown
## 安装

不同 Agent 工具安装方式不同；如在多个工具中使用，请分别安装。

### 一键脚本（推荐）
```bash
curl -fsSL https://raw.githubusercontent.com/<owner>/<repo>/main/install.sh | bash -s -- <skill>
```

### 社区 CLI（skills.sh，支持 75+ agent 工具）
```bash
npx skills add <owner>/<repo> -s <skill>
```

### 宿主 marketplace
`/plugin marketplace add <owner>/<repo>` → `/plugin install <name>@<marketplace>`

### 手动
git clone --depth 1 … && cp -r <skill> ~/.agents/skills/

> [!IMPORTANT]
> 装完需新开会话生效（skills 目录在会话启动时扫描）。

### 验证
新会话里说"<一句能触发该 skill 的话>"，能自动进入工作流即安装成功。

### 更新
重跑同一条安装命令（旧版自动备份）。
```

## 呈现细节

- **badge 即按钮**：把徽章链到安装页/文档站（如 `[![skills.sh](https://skills.sh/b/<owner>/<repo>)](https://skills.sh/<owner>/<repo>)`）——前提是徽章服务确实收录了该仓库，否则会挂破图
- **顶部导航行**：标题下一行 `安装 · 文档 · 报告 Bug` 锚点链接（starship 模式）
- **锚点保护注释**：被外部链接引用的标题上方加 `<!-- this anchor is linked to from elsewhere, so avoid renaming it -->`（gh 模式）
- **demo 媒体前置且不占纵向空间**：`<img align="right" width="50%">` 浮动、`<picture>` 明暗双版（starship / uv 模式）
- 版本下限写在表格里（fzf："Debian 9+"），别让用户装完才发现不兼容
