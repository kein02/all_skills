# README 写作原则（调研结晶）

来源：Awesome README（约 90 个优秀示例归纳）、Standard Readme 规范、Make a README、GitHub 官方文档。

## 板块清单（按出现顺序）

| 优先级 | 板块 | 作用 |
|---|---|---|
| 必有 | Logo / 标题 | 第一印象 |
| 必有 | 徽章行 | 一行回答"项目活得好吗、能依赖吗"；≤5 个，只放有信息量的 |
| 必有 | 一句话定位 | 10 秒内说清"是什么、给谁用、解决什么"（Standard Readme：<120 字符） |
| 强烈建议 | 演示（截图/GIF/终端输出） | 展示 > 描述 |
| 必有 | 安装 / Quick Start | 一条可复制命令前置 + 验证方法 + 更新交代；渠道与实际分发一致（速查见 install-patterns.md） |
| 必有 | 使用示例 | 最小真实示例 + 预期输出 |
| 可选 | 目录（TOC） | 全文 <100 行可省略 |
| 可选 | 功能特性 / 架构 | bullet 列卖点；架构细节外链 |
| 可选 | FAQ / Troubleshooting | 按平台/场景分节，降低 issue 数量 |
| 可选 | Roadmap / 项目状态 | 停止维护必须明说，不静默弃坑 |
| 必有 | Contributing | 链 CONTRIBUTING.md + good first issue |
| 可选 | 致谢 / 赞助 / 生态 | 社会证明放尾部 |
| 必有 | License | **必须是最后一节** |

## 十条黄金原则

1. **前三屏决定生死**——logo + 一句话定位 + 可复制安装命令，是黄金三件套。
2. **把"读到上手"压到 10 秒内**——安装永远是一条可复制命令首选；一个代码块只含一种环境；装完紧跟验证方法（跑示例 / 开新终端见效果 / 说一句触发 prompt）；更新与卸载有交代。分发渠道必须与实际一致（写 `pip install` 就得真发布到 PyPI，否则给 clone+构建路径）。
3. **面向新手写作**——写清依赖、版本要求、环境变量，消除每一步歧义；不假设读者是专家。
4. **展示优先于描述**——GIF/截图/真实终端输出胜过千字介绍。
5. **长内容外链**——README 只留"上手所需"，API、教程、changelog 移到 docs/wiki；标准是"用户无需读代码就能用起来"。
6. **用"活的"数据建立信任**——CI 徽章、Star History、贡献者头像墙，代替静态自夸。
7. **诚实的边界声明**——明确"什么不支持"；nvm 的诚实声明大幅减少了 issue。
8. **贡献入口低门槛 + 规则清晰**——说清是否接受 PR、需要什么环境、跑什么检查。
9. **仓库内用相对链接**——fork/clone 后不断链；GitHub 渲染上限 500 KiB。
10. **Readme Driven Development**——项目公开前先写 README；它同时是给维护者的需求说明。

## 跨类型铁律（31 个高星仓库共性）

1. **README 的角色由"它回答什么问题"决定**：自足（库）→入口（框架）→手册（CLI/AI 应用/插件）→枢纽（self-hosted）→目录（内容库）→索引（awesome）→治理（运行时）→名片（profile）。写之前先定角色，角色决定篇幅。
2. **项目越成熟，README 越短**：immich 正文 5KB、django 54 行、next.js 50 行——深度内容全部下沉 docs 站。
3. **价值证明前置，社会证明收尾**：bench 表/截图/量化承诺放开头，贡献者墙/Star History/致谢放结尾。
4. **警示必须内联**：版本约束、生产警告、合规声明写在正文显眼处（加粗或 `> [!WARNING]`），不外链。
5. **规模一大就上自动化**：死链 CI（awesome）、标记自动生成文档（yt-dlp）、data 仓库分离——手工维护长 README 必腐烂。

## 反模式（交付前对照排查）

- ❌ 文字墙：无演示、无目录、无导航的大段文本
- ❌ 徽章堆砌成噪音
- ❌ 缺安装步骤或缺 License（"太长总比太短好"）
- ❌ 示例不给预期输出、脱离真实场景
- ❌ 把实现细节塞进 README（用户要的是"怎么用"不是"怎么写的"）
- ❌ 说不清解决什么问题
- ❌ 静默弃坑不标注状态
- ❌ 安装方式与实际分发渠道不符（写 `pip install` 却没发布到 PyPI）；只说"clone 后自行配置"没有具体命令
- ❌ 多平台/多宿主命令混在一个代码块里，用户复制到自己的环境直接报错
- ❌ 装完不告诉用户怎么验证、怎么更新
- ❌ 链接文字跨多行导致渲染失效；用绝对链接在 fork 后断链

## 徽章速查（shields.io）

```markdown
![npm](https://img.shields.io/npm/v/包名)
![pypi](https://img.shields.io/pypi/v/包名)
![license](https://img.shields.io/badge/license-MIT-green)
![build](https://github.com/OWNER/REPO/actions/workflows/ci.yml/badge.svg)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)]
```

## 模板骨架（通用底座，按类型蓝图增删）

```markdown
<div align="center">

# 项目名
一句话定位（是什么、给谁、解决什么）

[Demo GIF]

![badge](version) ![badge](build) ![badge](license)

[安装](#安装) · [文档](链接) · [报告 Bug](链接)

</div>

## ✨ 特性
- 卖点 1
- 卖点 2

## 🚀 快速开始
```bash
一行可复制的安装命令
```

## 📦 使用示例
最小真实示例 + 预期输出

## 📖 文档
深入内容 → 外链 docs / wiki

## 🤝 参与贡献
欢迎 PR！请先读 [CONTRIBUTING.md](CONTRIBUTING.md)，从 [good first issue](链接) 开始

## 📄 License
[MIT](LICENSE)
```

## 中英文项目风格差异（可选借鉴）

- 海外项目（nvm/ollama）：极少营销元素，重 troubleshooting、环境变量文档、诚实的能力边界声明
- 中文高星项目：双语切换链接放顶部、`<details>` 折叠长图表、Star History 趋势图、案例展示墙、打赏/公众号链路、统一幽默人设（Oh My Zsh 和 HowToCook 证明"有梗"本身就是记忆点）
- 写中文项目 README 时可适度借鉴后者，但营销元素要等用户明确要再加
