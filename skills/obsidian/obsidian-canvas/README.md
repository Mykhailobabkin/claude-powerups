# Obsidian Canvas

**Teach Claude how to create JSON Canvas files for Obsidian.**

A [Claude Code](https://docs.anthropic.com/en/docs/claude-code) skill that gives Claude a complete reference for `.canvas` files — nodes, edges, groups, and visual layouts. Part of the [Obsidian collection](../).

---

## The Problem

Obsidian's `.canvas` files use the JSON Canvas spec — a specific JSON format with strict requirements for node types, edge connections, ID formats, and coordinate systems. Without a reference, Claude generates invalid canvas files with wrong node schemas, broken edges, or malformed IDs.

## The Solution

This skill is a comprehensive reference for the JSON Canvas 1.0 specification. Claude loads it when creating or editing `.canvas` files, producing valid canvases that render correctly in Obsidian.

## What's Covered

- **4 node types** — Text (markdown content), file (vault references), link (external URLs), group (visual containers)
- **Edge system** — Connections between nodes with directional sides, arrow styles, colors, and labels
- **Color system** — Hex colors and 6 preset colors (red, orange, yellow, green, cyan, purple)
- **Layout rules** — Coordinate system, z-indexing, spacing recommendations, group padding
- **ID format** — 16-character lowercase hex strings
- **4 complete examples** — Simple text nodes, project board (Kanban), research canvas, flowchart with branching

## Installation

**Option A — Install all power-ups:**

```bash
git clone https://github.com/Mykhailobabkin/claude-powerups.git
cd claude-powerups
./install.sh
```

**Option B — Install just this skill:**

```bash
git clone https://github.com/Mykhailobabkin/claude-powerups.git
mkdir -p ~/.claude/skills
cp claude-powerups/skills/obsidian/obsidian-canvas/SKILL.md ~/.claude/skills/obsidian-canvas.md
```

## How It Works

This is a **passive reference skill** — Claude loads it automatically when working with `.canvas` files or when you mention Canvas files, mind maps, or flowcharts in the context of Obsidian. No command to invoke; it activates based on context.

## Related Skills

- [vault-setup](../vault-setup/) — Interactive wizard to create a full Obsidian vault
- [obsidian-markdown](../obsidian-markdown/) — Reference for Obsidian-flavored markdown syntax
- [obsidian-bases](../obsidian-bases/) — Reference for `.base` database views

## Credits

Created by [Mykhailo Babkin](https://x.com/babkin_ai)

Built with [Claude Code](https://docs.anthropic.com/en/docs/claude-code)

## License

MIT
