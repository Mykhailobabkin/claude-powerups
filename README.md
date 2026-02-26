# Claude Power-Ups

**Skills that make Claude Code actually useful.** Each power-up is a plug-and-play skill that adds new capabilities to your Claude Code setup.

## Available Power-Ups

### Obsidian Collection

4 skills that make Claude fluent in [Obsidian](https://obsidian.md). [Collection overview →](skills/obsidian/)

| Power-Up | Type | What It Does |
|----------|------|-------------|
| [vault-setup](skills/obsidian/vault-setup/) | Interactive wizard | Creates a full Obsidian vault with GitHub backup and Claude Code integration. `/vault-setup` |
| [obsidian-markdown](skills/obsidian/obsidian-markdown/) | Passive reference | Teaches Claude every Obsidian-flavored markdown feature — wikilinks, embeds, callouts, properties, tags |
| [obsidian-bases](skills/obsidian/obsidian-bases/) | Passive reference | Teaches Claude to create `.base` files with views, filters, formulas, and summaries |
| [obsidian-canvas](skills/obsidian/obsidian-canvas/) | Passive reference | Teaches Claude to create `.canvas` files with nodes, edges, groups, and layouts |

## Quick Install

```bash
git clone https://github.com/Mykhailobabkin/claude-powerups.git
cd claude-powerups
./install.sh
```

This copies all skills to `~/.claude/skills/`. Start a new Claude Code session and they're ready to use.

### Install a Single Skill

If you only want one:

```bash
mkdir -p ~/.claude/skills
cp skills/obsidian/vault-setup/SKILL.md ~/.claude/skills/vault-setup.md
```

Replace the path with whichever skill you want. The installed filename becomes the skill name.

## What Are Claude Code Skills?

Skills are markdown files that teach Claude new workflows. Drop a `.md` file into `~/.claude/skills/` and Claude gains a new capability — no plugins, no APIs, no config.

There are two types:

- **Interactive skills** have a slash command (e.g., `/vault-setup`). You invoke them and Claude runs an interactive workflow.
- **Passive reference skills** load automatically based on context. When Claude sees you're editing an Obsidian `.base` file, it loads the `obsidian-bases` reference without you asking.

## Contributing

Have an idea for a power-up? [Open an issue](https://github.com/Mykhailobabkin/claude-powerups/issues) or submit a PR.

### Skill Structure

Skills live under `skills/`, optionally grouped into collections:

```
skills/
├── collection-name/            ← Collection folder (optional)
│   ├── README.md               ← Collection overview
│   ├── skill-one/
│   │   ├── SKILL.md            ← The skill file (required)
│   │   ├── README.md           ← Documentation (recommended)
│   │   └── examples/           ← Examples and references (optional)
│   └── skill-two/
│       ├── SKILL.md
│       └── README.md
└── standalone-skill/           ← Skills can also live at the top level
    ├── SKILL.md
    └── README.md
```

The installer finds every `SKILL.md` at any depth and installs it using the parent directory name as the skill name.

## Credits

Built by [Mykhailo Babkin](https://x.com/babkin_ai) with Claude Code.

## License

MIT
