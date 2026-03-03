# Claude Power-Ups

**Skills that make Claude Code actually useful.** Each power-up is a plug-and-play skill that adds new capabilities to your Claude Code setup.

## Available Power-Ups

### Personal OS Plugin

Build a complete Personal OS — an Obsidian vault with SQLite databases, Python scripts, and Obsidian Bases for managing your entire life. [Plugin overview →](plugins/personal-os/)

| Power-Up | Type | What It Does |
|----------|------|-------------|
| [personal-os:setup](plugins/personal-os/skills/setup/) | Interactive wizard | Builds a full Personal OS vault from scratch or migrates an existing one. `/personal-os:setup` |
| [personal-os:scan](plugins/personal-os/skills/scan/) | Interactive workflow | Scans any Obsidian vault and produces a structured discovery report. `/personal-os:scan` |

### Obsidian Skills

4 skills that make Claude fluent in [Obsidian](https://obsidian.md). Used as companions by the Personal OS plugin. [Collection overview →](skills/obsidian/)

| Power-Up | Type | What It Does |
|----------|------|-------------|
| [obsidian-cleanup](skills/obsidian/obsidian-cleanup/) | Interactive workflow | Comprehensive vault health check — frontmatter, links, naming, bases. `/obsidian-cleanup` |
| [obsidian-markdown](skills/obsidian/obsidian-markdown/) | Passive reference | Teaches Claude every Obsidian-flavored markdown feature — wikilinks, embeds, callouts, properties, tags |
| [obsidian-bases](skills/obsidian/obsidian-bases/) | Passive reference | Teaches Claude to create `.base` files with views, filters, formulas, and summaries |
| [obsidian-canvas](skills/obsidian/obsidian-canvas/) | Passive reference | Teaches Claude to create `.canvas` files with nodes, edges, groups, and layouts |

> **Note:** `/vault-setup` has been replaced by `/personal-os:setup`, which does everything vault-setup did and more (SQLite databases, Python scripts, data layer design).

A plugin that builds a complete Personal OS — an Obsidian vault with SQLite databases, Python scripts, and Obsidian Bases for managing your entire life. [Plugin overview →](plugins/personal-os/)

| Power-Up | Type | What It Does |
|----------|------|-------------|
| [personal-os:setup](plugins/personal-os/skills/setup/) | Interactive wizard | Builds a full Personal OS vault from scratch or migrates an existing vault. `/personal-os:setup` |
| [personal-os:scan](plugins/personal-os/skills/scan/) | Interactive workflow | Scans any Obsidian vault and produces a structured discovery report. `/personal-os:scan` |

## Quick Install

```bash
git clone https://github.com/Mykhailobabkin/claude-powerups.git
cd claude-powerups
./install.sh
```

This installs skills to `~/.claude/skills/` and shows how to load plugins.

### Load the Personal OS Plugin

Plugins use Claude Code's native plugin system:

```bash
claude --plugin-dir ./plugins/personal-os
```

Then run `/personal-os:setup` to start the wizard.

### Install a Single Skill

```bash
mkdir -p ~/.claude/skills
cp -r skills/obsidian/obsidian-bases ~/.claude/skills/obsidian-bases
```

Replace the path with whichever skill you want.

## What Are Skills and Plugins?

**Skills** are markdown files that teach Claude new workflows. Drop one into `~/.claude/skills/` and Claude gains a new capability — no APIs, no config.

- **Interactive skills** have a slash command (e.g., `/obsidian-cleanup`). You invoke them and Claude runs a workflow.
- **Passive reference skills** load automatically based on context. When Claude edits a `.base` file, it loads `obsidian-bases` without you asking.

**Plugins** bundle multiple related skills with templates and scripts. They use Claude Code's native plugin system with namespaced commands (e.g., `/personal-os:setup`).

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

### Plugin Structure

Plugins bundle multiple related skills with templates and scripts:

```
plugins/
└── plugin-name/
    ├── .claude-plugin/
    │   └── plugin.json          ← Manifest (name, description, skills)
    ├── README.md                ← Documentation
    ├── CLAUDE.md                ← Project docs for Claude
    ├── skills/
    │   ├── skill-one/
    │   │   └── SKILL.md
    │   └── skill-two/
    │       └── SKILL.md
    ├── templates/               ← File templates used by skills
    └── scripts/                 ← Script templates used by skills
```

Plugins use Claude Code's native plugin system. Load with `claude --plugin-dir ./plugins/plugin-name`. Skills are auto-namespaced (e.g., `/personal-os:setup`).

## Credits

Built by [Mykhailo Babkin](https://x.com/babkin_ai) with Claude Code.

## License

MIT
