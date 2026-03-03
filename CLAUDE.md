# Claude Powerups — Guide for Claude

## What This Repo Is

Open-source collection of Claude Code skills and plugins. Two categories:
- **Personal OS Plugin** (`plugins/personal-os/`) — interactive wizard for building Obsidian vaults with SQLite + Python scripts
- **Obsidian Skills** (`skills/obsidian/`) — 4 standalone skills for Obsidian fluency

## Repo Structure

```
claude-powerups/
├── .claude-plugin/
│   ├── plugin.json              ← Repo-level plugin metadata
│   └── marketplace.json         ← Marketplace catalog (for /plugin marketplace add)
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
│       ├── obsidian-cleanup/    ← /obsidian-cleanup
│       ├── obsidian-markdown/   ← Passive reference
│       ├── obsidian-bases/      ← Passive reference
│       └── obsidian-canvas/     ← Passive reference
├── install.sh                   ← Installs skills to ~/.claude/skills/
└── README.md
```

## Key Conventions

- **Skills** are single SKILL.md files. Parent directory name = skill name.
- **Plugins** bundle skills with templates/scripts under `.claude-plugin/plugin.json`.
- **Templates** use `{{placeholder}}` with Handlebars-style `{{#each}}` / `{{#if}}` blocks.
- **Script templates** use `.py.tmpl` extension — Claude fills in domain-specific content.
- **Everything is universal** — no hardcoded user-specific content. All content is discovered through interviews or scans.

## Installation Methods

1. **Marketplace**: `/plugin marketplace add Mykhailobabkin/claude-powerups` → `/plugin install personal-os@claude-powerups`
2. **Direct load**: `claude --plugin-dir ./plugins/personal-os`
3. **Skills only**: `./install.sh` copies skills to `~/.claude/skills/`

## Git Conventions

- Branch from `main`
- Use naming: `feature/`, `fix/`, `hotfeature/`, `hotfix/`, `design/`
- Create PRs, never push directly to main
