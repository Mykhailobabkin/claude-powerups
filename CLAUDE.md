# Claude Powerups — Guide for Claude

## Vault Context

Vault path: `~/BRAIN/Work/Tools/Claude Powerups/project.md`

## Architecture

Open-source collection of Claude Code skills and plugins. Two categories:
- **Personal OS Plugin** (`plugins/personal-os/`) — interactive wizard for building Obsidian vaults with SQLite + Python scripts
- **Obsidian Skills** (`skills/obsidian/`) — 4 standalone skills for Obsidian fluency

```
claude-powerups/
├── .claude-plugin/
│   ├── plugin.json              ← Repo-level plugin metadata
│   └── marketplace.json         ← Marketplace catalog (v1.0.0)
├── plugins/
│   └── personal-os/             ← Personal OS plugin
│       ├── .claude-plugin/plugin.json
│       ├── CLAUDE.md            ← Plugin-specific guide for Claude
│       ├── skills/setup/        ← /personal-os:setup wizard
│       ├── skills/scan/         ← /personal-os:scan scanner
│       ├── templates/           ← File templates ({{placeholder}} syntax)
│       └── scripts/             ← Python script templates (.py.tmpl)
├── skills/
│   └── obsidian/                ← Obsidian skill collection
│       ├── obsidian-cleanup/    ← /obsidian-cleanup (active skill)
│       ├── obsidian-markdown/   ← Passive reference
│       ├── obsidian-bases/      ← Passive reference
│       └── obsidian-canvas/     ← Passive reference
├── install.sh                   ← Installs skills to ~/.claude/skills/
└── README.md
```

## Key Files

| File | Purpose |
|------|---------|
| `install.sh` | Finds all `SKILL.md` files, copies skill dirs to `~/.claude/skills/`, strips READMEs |
| `.claude-plugin/marketplace.json` | Marketplace catalog for `/plugin marketplace add` |
| `plugins/personal-os/CLAUDE.md` | Plugin-specific guide — design decisions, data layers, testing |
| `plugins/personal-os/skills/setup/SKILL.md` | Main wizard (bootstrap + migrate modes) |
| `plugins/personal-os/skills/scan/SKILL.md` | Vault scanner |
| `skills/obsidian/obsidian-cleanup/SKILL.md` | `/obsidian-cleanup` — vault health audit |

## Patterns & Conventions

- **Skills** are single `SKILL.md` files. Parent directory name = skill name.
- **Plugins** bundle skills with templates/scripts under `.claude-plugin/plugin.json`.
- **Templates** use `{{placeholder}}` with Handlebars-style `{{#each}}` / `{{#if}}` blocks.
- **Script templates** use `.py.tmpl` extension — Claude fills in domain-specific content at runtime.
- **Everything is universal** — no hardcoded user-specific content. All content is discovered through interviews or scans.
- **Three data layers** (Personal OS) — SQLite (timestamped numeric), Obsidian Bases (structured notes), plain markdown (freeform).

## Installation Methods

1. **Marketplace**: `/plugin marketplace add Mykhailobabkin/claude-powerups` then `/plugin install personal-os@claude-powerups`
2. **Direct load**: `claude --plugin-dir ./plugins/personal-os`
3. **Skills only**: `./install.sh` copies skills to `~/.claude/skills/`

## Dev Commands

```bash
# Install skills locally
./install.sh

# Test plugin locally
claude --plugin-dir ./plugins/personal-os

# Check what install.sh would find
find skills -name "SKILL.md" -type f | sort
```

## Deploy

- **GitHub:** `Mykhailobabkin/claude-powerups` (public)
- **No CI/CD** — manual releases, users install via marketplace or `install.sh`

## Git Conventions

- Branch from `main`
- Use naming: `feature/`, `fix/`, `hotfeature/`, `hotfix/`, `design/`
- Create PRs, never push directly to main

## Gotchas

- **Claude Code HAS a native plugin system.** Don't reinvent — it exists since v1.0.33. Always check official docs before claiming a feature doesn't exist.
- **Everything must be universal.** No references to Misha's vault structure (BRAIN, Body, Brand, etc.) in templates. All content is discovered through interviews or scans.
- **Repo location.** The repo is at `~/Developer/personal/claude-powerups/`, not `~/claude-powerups/`.
- **vault-setup is retired.** `/personal-os:setup` is a superset of the old `/vault-setup` skill. Don't recreate it.
- **README duplication on merge.** After merging PRs, re-read the merged file to check for duplicates or merge artifacts.
