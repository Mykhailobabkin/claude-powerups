# Personal OS Plugin — Guide for Claude

## What This Is
A Claude Code plugin that builds Personal OS vaults with Obsidian + SQLite + Python scripts. Two skills: `/personal-os:setup` (interactive wizard) and `/personal-os:scan` (vault scanner).

## Plugin Structure

```
plugins/personal-os/
├── .claude-plugin/
│   └── plugin.json              ← Plugin manifest
├── skills/
│   ├── setup/
│   │   └── SKILL.md             ← Main wizard (bootstrap + migrate modes)
│   └── scan/
│       └── SKILL.md             ← Standalone scanner
├── templates/                   ← File templates ({{placeholder}} syntax)
│   ├── home.md                  ← Home.md template
│   ├── hub.md                   ← Section hub template
│   ├── base-view.base           ← .base file template
│   ├── task-file.md             ← Task file template
│   ├── gitignore.txt            ← .gitignore template
│   └── claude-md.md             ← CLAUDE.md template
└── scripts/                     ← Python script templates
    ├── init_db.py.tmpl           ← DB initializer pattern
    ├── log_entry.py.tmpl         ← CLI logger pattern
    ├── generate_overview.py.tmpl ← DB → markdown generator pattern
    └── update_all.py.tmpl        ← Orchestrator pattern
```

## Key Design Decisions

- **Universal** — No hardcoded domains, platforms, or user-specific content. Everything is discovered through the interview or scan.
- **Three data layers** — SQLite (timestamped numeric data), Obsidian Bases (structured notes with properties), plain markdown (freeform content). The decision tree in the setup skill determines which layer each domain gets.
- **Coder vs non-coder** — Coders get full Python scripts + SQLite. Non-coders get Bases-only mode with frontmatter-driven views.
- **Templates are patterns, not copies** — The SKILL.md instructs Claude to use templates as structural guides and fill in content dynamically based on user answers.

## Companion Skills
The setup wizard references these Obsidian skills when building vault files:
- `obsidian-markdown` — Wikilink and callout syntax
- `obsidian-bases` — .base file syntax for filters, formulas, views
- `obsidian-cleanup` — Used during verification phase

## Testing
Load the plugin for testing:
```bash
claude --plugin-dir ./plugins/personal-os
```
