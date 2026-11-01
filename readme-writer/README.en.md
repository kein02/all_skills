# readme-writer

English | [简体中文](README.md)

An Agent Skill: say one sentence to your Agent, and it writes a "high-star quality" README for your repository — first detecting the project type, then writing against the matching proven structure, and passing a quality checklist before delivery.

![type](https://img.shields.io/badge/type-agent--skill-blue) ![scope](https://img.shields.io/badge/scope-personal-green)

## The Problem It Solves

Most READMEs die in one of three ways: a wall of text nobody reads, a description nobody understands, or install steps nobody can run.

This skill's methodology comes from a hands-on research of **31 high-star repositories** (React, Vue, axios, django, node, ripgrep, bat, yt-dlp, immich, localsend, transformers, whisper, sd-webui, nanoGPT, hello-algo, developer-roadmap, awesome-selfhosted, superpowers, sqlmap, Marlin, Mindustry, nvm, ollama, and more) plus **4 authoritative guides** (Awesome README, Standard Readme, Make a README, GitHub official docs), distilled into two core ideas and an executable workflow:

> The README is a router, not documentation; the first three screens decide life or death (positioning line + install command + demo).

## Installation

Different agent tools install skills differently; if you use several, install in each. Pick one of the following:

**One-liner script** (copies into `~/.agents/skills/`, backs up old versions automatically):

```bash
curl -fsSL https://raw.githubusercontent.com/kein02/all_skills/main/install.sh | bash -s -- readme-writer
```

**Community CLI** (skills.sh, works with many agent tools):

```bash
npx skills add kein02/all_skills -s readme-writer
```

**Manual** (no other dependencies; for project-level install, put the folder under `<project>/.agents/skills/` instead):

```bash
git clone --depth 1 https://github.com/kein02/all_skills
mkdir -p ~/.agents/skills && cp -r all_skills/readme-writer ~/.agents/skills/
```

> [!IMPORTANT]
> You must start a **new session** after installing (the skills directory is scanned at session startup). In the current session you can force it with `/readme-writer`.

**Verify**: in a new session, say "write a README for this project" — if it automatically enters the workflow, the install worked.

**Update**: re-run the same install command (the old version is backed up as `readme-writer.bak.<timestamp>`).

## Usage

**Auto-triggering** — phrases with the following intent activate it automatically:

- "Write a README for this project"
- "Nobody understands my README, rewrite it"
- "I'm open-sourcing this project, prepare the docs"

**Manual** — type `/readme-writer` in ZCode (fallback when auto-triggering doesn't fire).

## Workflow

Once triggered, the Agent walks through 6 steps:

| Step | What it does | Key rule |
|---|---|---|
| 1. Recon | Reads package.json / pyproject.toml / tests / examples / CI configs, builds a "fact sheet" | Every fact must have a source — **no fabrication** |
| 2. Type detection | Uses the two-question heuristic to place the repo into one of 18 types and assign a role | Mixed projects are classified by the user's primary usage |
| 3. Apply blueprint | Follows the proven section order for that type | Install always up front; License always last |
| 4. Write | Follows the ten golden principles | Unverifiable info becomes `<!-- TODO -->`, never invented star counts or testimonials |
| 5. Self-check | Runs through the checklist | Relative links, ≤5 badges, <500 KiB rendered, no text walls |
| 6. Deliver | Writes README.md and reports | Explains the detected type and why; lists TODOs for you to fill |

### Supported Project Types (18)

Two-question heuristic: ① **What does the reader do first with it?** (decides type) ② **What question should the README answer?** (decides role and length — self-contained / entry / manual / hub / directory / index / governance / business-card)

| Group | Type | First thing with it | Reference repos |
|---|---|---|---|
| Code & Runtimes | Library / SDK | import it | axios, React |
| Code & Runtimes | Framework / Platform | scaffold a new project | django, TensorFlow |
| Code & Runtimes | Language runtime | pick a version, set up env | node |
| Tools & Apps | CLI tool | type commands | ripgrep, yt-dlp |
| Tools & Apps | Self-hosted app | deploy it | immich |
| Tools & Apps | Desktop / mobile app | download & install | localsend |
| AI & Academic | AI model / AI library | run the model | transformers, whisper |
| AI & Academic | AI app | "can my GPU run it" | sd-webui |
| AI & Academic | Paper reproduction | reproduce the paper numbers | nanoGPT |
| Content & Curation | Knowledge base / tutorial | start reading | hello-algo, HowToCook |
| Content & Curation | Learning roadmap | click a path | developer-roadmap |
| Content & Curation | awesome list | search for tools | awesome-selfhosted |
| Verticals | Plugin / Agent Skill | install into the host | superpowers |
| Verticals | Security tool | authorized testing | sqlmap, sherlock |
| Verticals | Hardware / embedded | flash firmware | Marlin |
| Verticals | Game | play it or build it | Mindustry |
| Verticals | dotfiles / config | copy it safely | mathiasbynens/dotfiles |
| Verticals | Profile README | get to know you | github-readme-stats users |

Full blueprints per type (section order, layout techniques, pitfalls) live in `references/project-types.md`; the five cross-type laws (role decides length, maturity shortens, proof first / social proof last, warnings inline, automate at scale) live in `references/principles.md`. Both are loaded on demand and stay out of everyday context.

## File Structure

```
readme-writer/
├── SKILL.md                      # Entry: triggering conditions + 6-step workflow (~100 lines)
└── references/                   # Loaded on demand, stays out of everyday context
    ├── project-types.md          # Detection signals + 18 blueprints
    ├── principles.md             # Section checklist, ten principles, anti-patterns, i18n, badge cheatsheet
    └── install-patterns.md       # Install/distribution cheatsheet (zero-friction seven + ecosystem commands)
```

## Customization

- To change a type's section order → edit the blueprint in `references/project-types.md`
- To adjust principles or anti-patterns → edit `references/principles.md`
- To change when it triggers → edit the `description` field in `SKILL.md` (it is the sole basis for auto-triggering)

## Known Limitations

- Language follows the current conversation; if the repo shows international-audience signals (English README/issues), it asks "Chinese / English / bilingual" first. Bilingual output follows the i18n convention: sibling files (README.en.md) with a bidirectional switch line under the title
- Assets that don't exist in the repo (screenshots, GIFs, donation links) are never fabricated — they come back as a TODO list for you to fill
- If a README already exists, it reads it first and preserves your links and badges; for repos not under git, it asks before overwriting
- To generate "real terminal output" for CLIs, it only runs safe read-only commands

## Feedback

If something goes wrong (wrong type detection, bad structure, trigger misses), open an issue in this repo with the target repo and the produced output attached, so the blueprints can be iterated.
