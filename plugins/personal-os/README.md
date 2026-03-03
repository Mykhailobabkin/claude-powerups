# Personal OS Plugin

**Build a complete Personal OS with Obsidian + SQLite + Python scripts.** An interactive wizard that designs and builds a vault tailored to your life — whether you code or not.

## What It Does

The Personal OS plugin transforms an Obsidian vault into a structured operating system for your life. It interviews you about your domains (work, health, learning, finance, creative, personal), then builds:

- **Folder structure** with section hubs and project files
- **Data layer** — SQLite databases for numeric tracking (coders) or Obsidian Bases for dynamic views (non-coders)
- **Python scripts** for logging entries and generating overview dashboards
- **Task board** with `.base` views for filtering and grouping
- **CLAUDE.md** so Claude Code understands your vault automatically
- **GitHub backup** with auto-sync via Obsidian Git

## Skills

| Skill | Command | What It Does |
|-------|---------|-------------|
| Setup Wizard | `/personal-os:setup` | Full interactive setup — bootstrap a new vault or migrate an existing one |
| Vault Scanner | `/personal-os:scan` | Scan any Obsidian vault and produce a structured discovery report |

## Install

**From the marketplace** (inside Claude Code):

```
/plugin marketplace add Mykhailobabkin/claude-powerups
/plugin install personal-os@claude-powerups
```

**Or load directly** (for development):

```bash
git clone https://github.com/Mykhailobabkin/claude-powerups.git
claude --plugin-dir ./claude-powerups/plugins/personal-os
```

Then run `/personal-os:setup` to start the wizard.

## Two Modes

### Bootstrap (new vault)
Start from scratch. The wizard interviews you, designs the architecture, and builds everything.

### Migrate (existing vault)
Already have a vault? The wizard scans it first, proposes improvements, and only makes changes you approve.

## The Data Layer Decision Tree

The wizard decides what storage layer to use for each domain:

| Question | If Yes → |
|----------|----------|
| Timestamped numeric data? | SQLite database |
| Logged regularly (daily/weekly)? | SQLite database |
| Need aggregate views (trends, averages)? | SQLite database |
| Structured notes with properties? | Obsidian Bases (.base views) |
| Freeform content? | Plain markdown |

Non-coders get Bases-only mode — no Python required.

## What Gets Generated

### For Coders (SQLite + Python)

Per data domain:
- `init_[domain]_db.py` — Creates the SQLite schema
- `log_[domain].py` — CLI for logging new entries
- `generate_[domain].py` — Reads DB → writes markdown overview
- `update_all.py` — Runs all generators

### For Everyone

- `Home.md` — Vault entry point with section links
- Section hubs with wikilinks and base view embeds
- `.base` files for dynamic views (tasks, projects, habits)
- `CLAUDE.md` with vault structure, naming conventions, and trigger phrases
- `.gitignore` for clean Git history

## Works With

This plugin uses the companion Obsidian skills when they're installed:

- **obsidian-markdown** — Correct wikilinks, callouts, and properties
- **obsidian-bases** — Valid `.base` file syntax
- **obsidian-cleanup** — Vault health checks after setup

## Credits

Built by [Mykhailo Babkin](https://x.com/babkin_ai) with Claude Code.
