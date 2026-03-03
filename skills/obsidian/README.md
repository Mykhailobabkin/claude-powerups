# Obsidian Skills

**4 skills that make Claude Code fluent in Obsidian.** Reference skills for syntax, an interactive health checker, and companion support for the [Personal OS plugin](../../plugins/personal-os/).

## Skills

| Skill | Type | What It Does |
|-------|------|-------------|
| [obsidian-cleanup](obsidian-cleanup/) | Interactive workflow | Comprehensive vault health check — frontmatter, links, naming, bases. `/obsidian-cleanup` |
| [obsidian-markdown](obsidian-markdown/) | Passive reference | Teaches Claude every Obsidian-flavored markdown feature (wikilinks, embeds, callouts, properties, etc.) |
| [obsidian-bases](obsidian-bases/) | Passive reference | Teaches Claude to create `.base` files with views, filters, formulas, and summaries |
| [obsidian-canvas](obsidian-canvas/) | Passive reference | Teaches Claude to create `.canvas` files with nodes, edges, groups, and layouts |

## How They Work

**Claude just knows Obsidian.** The three reference skills load automatically when Claude works with Obsidian files — no commands to run:

- Editing a `.md` file in your vault? Claude uses **obsidian-markdown** for correct wikilinks, callouts, and properties.
- Creating a `.base` file for a dynamic view? Claude uses **obsidian-bases** for valid filters, formulas, and view configs.
- Building a `.canvas` for a visual layout? Claude uses **obsidian-canvas** for correct node types, edges, and coordinates.

**Keep it healthy:** Run `/obsidian-cleanup` periodically to audit your vault — frontmatter, links, naming, plugin sync — and keep your CLAUDE.md in sync with reality.

**Build a full system:** Run `/personal-os:setup` from the [Personal OS plugin](../../plugins/personal-os/) to build a complete vault with SQLite databases, Python scripts, and structured sections. It uses these skills as companions.

## Install

```bash
git clone https://github.com/Mykhailobabkin/claude-powerups.git
cd claude-powerups
./install.sh
```

Or install individually — see each skill's README for single-skill install commands.
