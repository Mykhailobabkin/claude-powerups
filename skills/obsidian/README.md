# Obsidian Collection

**4 skills that make Claude Code fluent in Obsidian.** From creating a vault from scratch to writing perfect `.base` and `.canvas` files.

## Skills

| Skill | Type | What It Does |
|-------|------|-------------|
| [vault-setup](vault-setup/) | Interactive wizard | Creates a full Obsidian vault with GitHub backup and Claude Code integration |
| [obsidian-markdown](obsidian-markdown/) | Passive reference | Teaches Claude every Obsidian-flavored markdown feature (wikilinks, embeds, callouts, properties, etc.) |
| [obsidian-bases](obsidian-bases/) | Passive reference | Teaches Claude to create `.base` files with views, filters, formulas, and summaries |
| [obsidian-canvas](obsidian-canvas/) | Passive reference | Teaches Claude to create `.canvas` files with nodes, edges, groups, and layouts |

## How They Work Together

**Start here:** Run `/vault-setup` to create your vault. The wizard interviews you about your projects and builds a personalized Obsidian vault backed up to GitHub.

**Then Claude just knows Obsidian:** The three reference skills load automatically when Claude works with Obsidian files. No commands to run — Claude uses the right reference based on what file type you're editing:

- Editing a `.md` file in your vault? Claude uses **obsidian-markdown** for correct wikilinks, callouts, and properties.
- Creating a `.base` file for a dynamic view? Claude uses **obsidian-bases** for valid filters, formulas, and view configs.
- Building a `.canvas` for a visual layout? Claude uses **obsidian-canvas** for correct node types, edges, and coordinates.

## Install All

```bash
git clone https://github.com/Mykhailobabkin/claude-powerups.git
cd claude-powerups
./install.sh
```

Or install individually — see each skill's README for single-skill install commands.
