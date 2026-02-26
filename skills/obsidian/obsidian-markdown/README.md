# Obsidian Markdown

**Teach Claude every Obsidian-flavored markdown feature.**

A [Claude Code](https://docs.anthropic.com/en/docs/claude-code) skill that gives Claude a complete reference for Obsidian's extended markdown syntax. Part of the [Obsidian collection](../).

---

## The Problem

Claude knows standard markdown, but Obsidian adds dozens of features on top: wikilinks, embeds, callouts, block references, properties (frontmatter), and more. Without a reference, Claude generates broken syntax — wrong embed formats, missing callout types, incorrect property fields.

## The Solution

This skill is a comprehensive reference document that Claude loads when working with Obsidian files. It covers every Obsidian-specific syntax feature with correct examples, so Claude produces valid `.md` files that render perfectly in Obsidian.

## What's Covered

- **Wikilinks** — `[[Note]]`, `[[Note|Display]]`, `[[Note#Heading]]`, `[[Note#^block-id]]`
- **Embeds** — `![[Note]]`, `![[image.png|640x480]]`, `![[audio.mp3]]`, `![[doc.pdf#page=3]]`
- **Callouts** — All 13 types (note, tip, warning, bug, etc.), foldable, nested, custom CSS
- **Properties (frontmatter)** — All types: text, number, checkbox, date, datetime, list, links
- **Tags** — Inline `#tag`, nested `#parent/child`, frontmatter tags
- **Math** — Inline `$...$` and block `$$...$$` LaTeX
- **Mermaid diagrams** — Including class links for internal vault linking
- **Footnotes** — Numbered, named, and inline
- **Comments** — `%%hidden%%` for content hidden from preview
- **HTML in markdown** — `<details>`, `<kbd>`, custom `<div>` blocks

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
cp claude-powerups/skills/obsidian/obsidian-markdown/SKILL.md ~/.claude/skills/obsidian-markdown.md
```

## How It Works

This is a **passive reference skill** — Claude loads it automatically when working with Obsidian files or when you mention wikilinks, callouts, frontmatter, tags, or embeds. No command to invoke; it activates based on context.

## Related Skills

- [vault-setup](../vault-setup/) — Interactive wizard to create a full Obsidian vault
- [obsidian-bases](../obsidian-bases/) — Reference for `.base` database views
- [obsidian-canvas](../obsidian-canvas/) — Reference for `.canvas` visual files

## Credits

Created by [Mykhailo Babkin](https://x.com/babkin_ai)

Built with [Claude Code](https://docs.anthropic.com/en/docs/claude-code)

## License

MIT
