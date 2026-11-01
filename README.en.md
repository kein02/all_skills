# all_skills

English | [简体中文](README.md)

A collection of Agent skills accumulated through personal development and learning (works with ZCode, Claude Code, and any tool that supports the Agent Skills standard). Each skill lives in its own directory; one command installs it (see below).

## Skill Directory

| Skill | Description |
|---|---|
| [readme-writer](readme-writer/README.en.md) | **README Writer**: generates "high-star quality" READMEs for code repositories. Distilled from research on 31 high-star repos (React, Vue, immich, yt-dlp, transformers, superpowers, etc.) and 4 authoritative guides (Awesome README, Standard Readme, Make a README, GitHub docs): auto-detects the project type (library / CLI / app / AI / content collection / plugin — 18 types in total) and positions the README's role, applies the matching high-star blueprint, writes under ten golden principles, and passes a self-check before delivery. Anti-hallucination guardrail built in — every fact in the README must come from the repository itself. |

→ Click a skill name for its detailed docs (problem it solves, install, triggering, workflow, customization). Inside each skill folder: `SKILL.md` is the entry point read by the Agent, `README.md` is the human-readable usage doc, and `README.en.md` is the English version.

## Quick Install

One-liner (clones this repo and copies the skill into `~/.agents/skills/`, backing up any old version automatically):

```bash
curl -fsSL https://raw.githubusercontent.com/kein02/all_skills/main/install.sh | bash -s -- readme-writer
```

Alternatives:

```bash
# Community CLI (skills.sh; works with Claude Code, Cursor, and more agent tools)
npx skills add kein02/all_skills -s readme-writer

# Manual
git clone --depth 1 https://github.com/kein02/all_skills
mkdir -p ~/.agents/skills && cp -r all_skills/readme-writer ~/.agents/skills/
```

> [!IMPORTANT]
> You must start a **new session** after installing — the skills directory is scanned at session startup.

## Adding New Skills

Keep the "one skill per folder" structure:

- Folder name = skill name (lowercase kebab-case)
- Entry point is `SKILL.md`; the YAML frontmatter only needs `name` + `description` (the description defines when it triggers — it is the key to auto-triggering)
- Long content goes in `references/` (loaded on demand), scripts in `scripts/`, templates in `assets/`
- Provide both `README.md` (Chinese docs) and `README.en.md` (English docs), with a bidirectional language-switch line under each title
- Add a row to the table above when done
