# obsidian-auto

English | [简体中文](README.md)

An Agent Skill: one sentence scaffolds a three-layer Obsidian knowledge base (`raw/` + `wiki/`) and wires up two scheduled tasks — "daily organize" and "weekly health check" — at times you choose. Re-running only fills gaps; it never overwrites what you already have.

![type](https://img.shields.io/badge/type-agent--skill-blue) ![scope](https://img.shields.io/badge/scope-personal-green)

## What it solves

Three things usually stop people from keeping an Obsidian knowledge base alive:

- **Scaffolding is tedious** — creating folders, writing conventions, defining page structure; half an hour gone before a single note lands.
- **Nobody maintains it** — material piles up in `raw/`, gets organized once, then never again.
- **Every agent needs a redo** — whatever you set up in Claude Code has to be rebuilt in Codex.

This skill packages structure and maintenance together: one command creates the directories plus four convention files (`AGENTS.md`, `README.md`, `index.md`, `log.md`), then attaches the two recurring tasks to a scheduler. The same skill installs into 12 agents.

## Install

Each agent tool has its own skills directory; if you use several, install separately. Pick one:

**One-liner** (copies into `~/.agents/skills/`, backs up any previous version):

```bash
curl -fsSL https://raw.githubusercontent.com/kein02/all_skills/main/install.sh | bash -s -- obsidian-auto
```

**Community CLI** (skills.sh, supports multiple agent tools):

```bash
npx skills add kein02/all_skills -s obsidian-auto
```

**Manual** (use this for project scope too — drop it into `<project>/.agents/skills/`):

```bash
git clone --depth 1 https://github.com/kein02/all_skills
mkdir -p ~/.agents/skills && cp -r all_skills/obsidian-auto ~/.agents/skills/
```

> [!IMPORTANT]
> Start a **new session** after installing — the skills directory is scanned at startup. In the current session, invoke `/obsidian-auto` explicitly.

**Verify** — in a new session, say:

> Use obsidian-auto to create a knowledge base at `D:/Obsidian/reading-notes`, organize daily at 8am, check weekly on Sunday at 9pm.

If it enters the workflow, you're set.

**Update**: rerun the same install command (the old copy is backed up as `obsidian-auto.bak.<timestamp>`).

**Requirements**: Python 3.8+, standard library only, no pip; Windows / macOS / Linux.

## Usage

**Auto-trigger** — any of these phrasings activates it:

- "Create a new Obsidian knowledge base"
- "Build me a vault like my AI-learning one"
- "My vault structure is a mess / missing folders — fix it"
- "Add daily organization and weekly checks to this vault"

**Manual** — `/obsidian-auto` where slash commands exist (Codex: `$obsidian-auto`).

## What it creates

```
your-vault/
├── raw/                       source material: articles, papers, notes (read-only)
├── wiki/
│   ├── concepts/              concept pages: methods, ideas, by topic
│   ├── entities/              entity pages: tools, people, platforms, by object
│   └── sources/               one summary page per source
├── AGENTS.md                  working rules the agent reads first
├── index.md                   vault index, maintained by the agent
├── log.md                     operation log, the incremental baseline
└── README.md                  the map for humans
```

Two scheduled tasks, always at times you specify:

| Task | What it does | Schedule |
|---|---|---|
| Daily organize | Reads `AGENTS.md`, diffs `raw/` against `log.md`, folds new or changed material into `wiki/`, updates `index.md` and `log.md`; exits immediately when nothing changed | Daily, at your time |
| Weekly health check | Reports broken links, orphan pages, conflicting conclusions; **never modifies files during the check** | Weekly, on your day and time |

> Times have no defaults. If you don't say, it asks — it won't pick for you.

## Command reference

### `scaffold.py` — create the structure

| Flag | Purpose |
|---|---|
| `--path` | Absolute vault path (required) |
| `--name` / `--domain` / `--material-desc` | Vault name, topic, what goes in `raw/` — drives all generated copy |
| `--daily-time` / `--weekly-time` | **Required** trigger times |
| `--weekly-day` | Day for the weekly task, default `MO` |
| `--profile` | `standard` (three categories) or `minimal` (sources only) |
| `--extra-category "name:description"` | Append a custom category, repeatable |
| `--automations off` | Structure only, no scheduled tasks |
| `--dry-run` / `--verify` / `--force` / `--create-parents` | Preview / check / back up before overwrite / create parents |

```bash
python scripts/scaffold.py --path "D:/Obsidian WH/new-vault" --name "new-vault" --domain "AI learning" \
  --daily-time "08:00" --weekly-day SU --weekly-time "21:00"
```

Output is JSON: `created_files`, `skipped_files`, `changed`, `automations`, `summary_lines`.

### `schedule.py` — attach the tasks to a scheduler

| Platform | Artifacts |
|---|---|
| `workbuddy` | JSON payload for `automation_update` |
| `cron` | `crontab.txt` + wrapper scripts |
| `schtasks` | Windows Task Scheduler script (`.ps1`, UTF-8 BOM) + `.cmd` wrappers |
| `launchd` | macOS LaunchAgent plists |
| `json` | Platform-neutral task spec including full prompts |

```bash
python scripts/schedule.py --vault "D:/Obsidian WH/new-vault" --platform auto \
  --daily-time "08:00" --weekly-day SU --weekly-time "21:00" --write
```

`auto` picks by OS (Windows → Task Scheduler, macOS → launchd, Linux → cron); `--runner` sets the CLI that executes a task (defaults to `claude -p`).

### `install.py` — install into other agents

```bash
python scripts/install.py --target all --scope user           # every supported host on this machine
python scripts/install.py --target cursor --scope project --project "D:/repo"
```

Targets: `claude` `codex` `cursor` `gemini` `copilot` `windsurf` `cline` `roo` `opencode` `goose` `kiro` `workbuddy`, or `all`. Identical content is reported as `unchanged`; differences require `--force` and are backed up first.

## Idempotency and safety

- **Add only, never rewrite**: existing directories and files are skipped; `raw/` and existing wiki pages are never touched.
- **Backup before overwrite**: only an explicit `--force` replaces the four convention files, and it writes `*.bak-<timestamp>` first.
- **Your times, not defaults**: missing `--daily-time` / `--weekly-time` exits with code 2 instead of silently picking a slot.
- **No silent system changes**: cron / Task Scheduler / launchd entries are printed for approval before registration.
- **Safe to rerun**: a second run reports `changed=false` and creates no duplicate log entries or tasks.

## Cross-agent compatibility

Follows the open Agent Skills spec and relies on `name` + `description` only, so the folder works unchanged everywhere.

| Host | Skills directory | Invocation |
|---|---|---|
| Claude Code | `~/.claude/skills/` | `/obsidian-auto` |
| Codex CLI | `~/.codex/skills/` | `$obsidian-auto` |
| Cursor | `~/.cursor/skills/` | description-triggered (reload window after install) |
| WorkBuddy | `~/.workbuddy/skills/` | description-triggered |
| Others (Gemini, Copilot, Windsurf, Cline, Roo, OpenCode, Goose, Kiro) | see `references/agent-compat.md` | description-triggered |

## File structure

```
obsidian-auto/
├── SKILL.md                    entry: triggers + six-step workflow
├── scripts/
│   ├── scaffold.py             idempotent scaffold generator (validate / dry-run / verify / force)
│   ├── schedule.py             scheduler generator (workbuddy / cron / schtasks / launchd / json)
│   ├── install.py              multi-host installer
│   └── tasks.py                shared task definitions (prompts / times)
├── assets/templates/           AGENTS / README / index / log templates
└── references/
    ├── parameters.md           full flags, exit codes, idempotency and reconciliation rules
    └── agent-compat.md         per-agent directories, fields and invocation differences
```

## Known limits

- Structure only — **it does not move content**; drop material into `raw/` and the daily task takes it from there.
- Task prompts embed absolute paths — **rerun after moving the vault** to refresh them.
- OS scheduling needs the matching CLI installed (`claude -p`, `codex exec`, `gemini -p`) and able to read a prompt from stdin.
- Registering Windows tasks requires an elevated PowerShell session.
- Obsidian's default `欢迎.md` is never deleted automatically; you get a reminder instead.
- Copy is generated for a general/academic audience; domain wording is tuned via `--domain` and `--material-desc`, with no per-industry templates.

## Feedback

Open an issue in this repository with the command you ran and the JSON output if something goes wrong (unexpected structure, tasks not registered, triggering issues on a specific host).
