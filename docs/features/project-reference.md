---
title: "Claude Powerups project reference"
status: active
created: 2026-09-06
last_updated: 2026-09-06
tags: [project-documentation]
---

> Project reference migrated from the earlier note. Roadmap statuses and published-post counts describe that note’s date, not a fresh live audit.

# Claude Powerups

Open-source Claude Code skills and plugins. GitHub: `Mykhailobabkin/claude-powerups` (public).

## Components

### Personal OS Plugin (`plugins/personal-os/`)
Interactive wizard that builds Obsidian vaults with SQLite + Python scripts. Two skills:
- `/personal-os:setup` — bootstrap new vault or migrate existing one
- `/personal-os:scan` — scan and analyze existing vault structure

### Obsidian Skills (`skills/obsidian/`)
4 standalone skills for Obsidian fluency:
- `obsidian-cleanup` — vault health audit (active skill, used as `/obsidian-cleanup`)
- `obsidian-markdown` — wikilink and callout syntax reference
- `obsidian-bases` — .base file syntax for filters, formulas, views
- `obsidian-canvas` — canvas file format reference

## Related

- Blog article: Advanced Claude Code Setup — Published article covering skills, CLAUDE.md patterns, hooks
- Blog article: Claude Code Memory — Published article on Obsidian-based memory architecture
- Skill Evolution Ideas — Concept note on strategic compaction and /evolve command

## Install

```bash
# Skills only
./install.sh

# Plugin (local testing)
claude --plugin-dir ./plugins/personal-os

# Marketplace
/plugin marketplace add Mykhailobabkin/claude-powerups
```
