# Claude Power-Ups

**Skills and plugins that make Claude Code actually useful.** Drop them in and Claude gains new capabilities — YouTube video analysis, Obsidian fluency, vault building, and more.

## What's Inside

### Personal OS Plugin

An interactive wizard that builds a complete Personal OS — an Obsidian vault with SQLite databases, Python scripts, and dynamic views, tailored to your life. [Read more →](plugins/personal-os/)

| Command | What It Does |
|---------|-------------|
| `/personal-os:setup` | Interactive wizard — bootstrap a new vault or migrate an existing one |
| `/personal-os:scan` | Scan any Obsidian vault and produce a structured discovery report |

### YouTube Analyze Skill

Pull transcripts from YouTube videos and compile insights into articles, summaries, or comparisons. No API keys required. [Read more →](skills/youtube-analyze/)

| Command | What It Does |
|---------|-------------|
| `/youtube-analyze` | Pass YouTube URLs → pulls transcripts → analyzes content → produces article/summary |

**How it works:** A Python script (`youtube-transcript-api` + `yt-dlp`) fetches transcripts, then Claude analyzes them in-context. Handles 30+ videos in a single session.

### Obsidian Skills

4 skills that make Claude fluent in [Obsidian](https://obsidian.md). Load automatically when relevant. [Read more →](skills/obsidian/)

| Skill | What It Does |
|-------|-------------|
| `obsidian-cleanup` | Vault health check — frontmatter, links, naming, bases. Run with `/obsidian-cleanup` |
| `obsidian-markdown` | Teaches Claude wikilinks, embeds, callouts, properties, and tags |
| `obsidian-bases` | Teaches Claude to create `.base` files with views, filters, and formulas |
| `obsidian-canvas` | Teaches Claude to create `.canvas` files with nodes, edges, and groups |

## Install

### Option 1: Plugin Marketplace (recommended)

Inside a Claude Code session, run:

```
/plugin marketplace add Mykhailobabkin/claude-powerups
```

Then install the Personal OS plugin:

```
/plugin install personal-os@claude-powerups
```

That's it. Run `/personal-os:setup` to start the wizard.

### Option 2: Clone and Install Everything

```bash
git clone https://github.com/Mykhailobabkin/claude-powerups.git
cd claude-powerups
./install.sh
```

This installs all skills to `~/.claude/skills/`. For the YouTube skill, also install the Python dependency:

```bash
pip3 install youtube-transcript-api
```

For the Personal OS plugin, start Claude with:

```bash
claude --plugin-dir ./plugins/personal-os
```

### Option 3: Install a Single Skill

```bash
git clone https://github.com/Mykhailobabkin/claude-powerups.git
mkdir -p ~/.claude/skills

# Obsidian skill (pick one):
cp -r claude-powerups/skills/obsidian/obsidian-bases ~/.claude/skills/obsidian-bases

# YouTube analyzer:
cp -r claude-powerups/skills/youtube-analyze ~/.claude/skills/youtube-analyze
pip3 install youtube-transcript-api
```

## How It Works

**Skills** are markdown files that teach Claude new capabilities. Drop one into `~/.claude/skills/` and it just works — no APIs, no config.

- **Interactive skills** have a slash command (e.g., `/obsidian-cleanup`). You run them and Claude walks you through a workflow.
- **Passive skills** load automatically based on context. Edit a `.base` file and Claude already knows the syntax.

**Plugins** bundle related skills with templates and scripts. They use Claude Code's native plugin system and provide namespaced commands like `/personal-os:setup`.

## Contributing

Have an idea for a power-up? [Open an issue](https://github.com/Mykhailobabkin/claude-powerups/issues) or submit a PR.

<details>
<summary>Skill and plugin structure</summary>

### Skills

```
skills/
├── collection-name/            ← Optional grouping folder
│   ├── README.md
│   ├── skill-one/
│   │   ├── SKILL.md            ← Required
│   │   ├── README.md
│   │   └── examples/
│   └── skill-two/
│       └── SKILL.md
└── standalone-skill/
    └── SKILL.md
```

The installer finds every `SKILL.md` at any depth and installs it using the parent directory name.

### Plugins

```
plugins/
└── plugin-name/
    ├── .claude-plugin/
    │   └── plugin.json         ← Plugin manifest
    ├── skills/
    │   └── skill-name/
    │       └── SKILL.md
    ├── templates/
    └── scripts/
```

Plugins use Claude Code's native plugin system. Skills are auto-namespaced (e.g., `/personal-os:setup`).

</details>

## Credits

Built by [Mykhailo Babkin](https://x.com/babkin_ai) with Claude Code.

## License

MIT
