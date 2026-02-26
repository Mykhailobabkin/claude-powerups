# Obsidian Bases

**Teach Claude how to create Obsidian Bases — database-like views of your notes.**

A [Claude Code](https://docs.anthropic.com/en/docs/claude-code) skill that gives Claude a complete reference for `.base` files, including views, filters, formulas, and summaries. Part of the [Obsidian collection](../).

---

## The Problem

Obsidian Bases is a relatively new feature with complex YAML syntax for filters, formulas, and view configuration. Claude's training data may not include the latest syntax, leading to broken `.base` files — wrong filter operators, invalid formula functions, or malformed YAML.

## The Solution

This skill is a comprehensive reference for the Bases YAML schema. Claude loads it when creating or editing `.base` files, producing valid configurations that work immediately in Obsidian.

## What's Covered

- **Complete YAML schema** — `filters`, `formulas`, `properties`, `summaries`, `views`
- **Filter syntax** — Single conditions, `and`/`or`/`not` nesting, all operators
- **Three property types** — Note (frontmatter), file metadata (`file.name`, `file.mtime`, etc.), formula
- **Formula functions** — `date()`, `duration()`, `now()`, `today()`, `if()`, `min()`, `max()`, `number()`, `link()`, `list()`, `file()`, `image()`, `icon()`, `html()`
- **Type-specific methods** — Date formatting, duration math, string manipulation, list operations, file queries
- **View types** — Table, cards, list, map — with groupBy, ordering, and per-view filters
- **15 built-in summaries** — Average, Min, Max, Sum, Range, Median, Stddev, Earliest, Latest, and more
- **4 complete examples** — Task tracker, reading list, project notes, daily notes index

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
cp claude-powerups/skills/obsidian/obsidian-bases/SKILL.md ~/.claude/skills/obsidian-bases.md
```

## How It Works

This is a **passive reference skill** — Claude loads it automatically when working with `.base` files or when you mention Bases, table views, card views, filters, or formulas in the context of Obsidian. No command to invoke; it activates based on context.

## Related Skills

- [vault-setup](../vault-setup/) — Interactive wizard to create a full Obsidian vault
- [obsidian-markdown](../obsidian-markdown/) — Reference for Obsidian-flavored markdown syntax
- [obsidian-canvas](../obsidian-canvas/) — Reference for `.canvas` visual files

## Credits

Created by [Mykhailo Babkin](https://x.com/babkin_ai)

Built with [Claude Code](https://docs.anthropic.com/en/docs/claude-code)

## License

MIT
