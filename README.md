# Claude Power-Ups

Skills and plugins that give Claude Code new capabilities. Drop them in and they just work.

## What's Inside

| Power-Up | Type | What It Does |
|----------|------|-------------|
| [YouTube Analyze](#youtube-analyze) | Skill | Pull transcripts from YouTube videos, compile insights into articles |
| [Personal OS](#personal-os) | Plugin | Build a complete personal system in Obsidian with databases and automation |
| [Obsidian Skills](#obsidian-skills) | Skills (4) | Make Claude fluent in Obsidian syntax, Bases, Canvas, and vault maintenance |

## Prerequisites

- [Claude Code](https://claude.ai/claude-code) installed and working
- **Python 3.9+** (required for YouTube Analyze and Personal OS)
- **yt-dlp** (required for YouTube Analyze, install with `brew install yt-dlp` or `pip3 install yt-dlp`)

## Quick Install

### Everything at once

```bash
git clone https://github.com/Mykhailobabkin/claude-powerups.git
cd claude-powerups
./install.sh
pip3 install youtube-transcript-api   # for YouTube Analyze
```

### Just one skill

```bash
git clone https://github.com/Mykhailobabkin/claude-powerups.git
mkdir -p ~/.claude/skills

# Pick what you need:
cp -r claude-powerups/skills/youtube-analyze ~/.claude/skills/
cp -r claude-powerups/skills/obsidian/obsidian-cleanup ~/.claude/skills/
```

### Via Plugin Marketplace

```
/plugin marketplace add Mykhailobabkin/claude-powerups
/plugin install personal-os@claude-powerups
```

---

## YouTube Analyze

Pull transcripts from any YouTube video and turn them into articles, summaries, or comparisons. No API keys. No OAuth. Just paste URLs.

**Command:** `/youtube-analyze`

**Example:**
```
/youtube-analyze
Analyze these videos and write an article about Claude Code workflows:
https://youtube.com/watch?v=abc123
https://youtube.com/watch?v=def456
https://youtu.be/ghi789
```

**What happens:**
1. A Python script pulls transcripts from each video (auto-generated or manual captions)
2. Claude gets all transcripts in-context (5 videos ~ 96K tokens, fits easily in 1M context)
3. Claude analyzes and produces whatever you asked for: article, comparison, summary, or answers to specific questions

**Requirements:**
- Python 3.9+
- `pip3 install youtube-transcript-api`
- `yt-dlp` (for fetching video titles)

**Limitations:**
- Videos must have captions (most do). No captions = no transcript.
- Age-restricted videos need authentication cookies.
- Auto-generated captions may have minor transcription errors.

---

## Personal OS

An interactive wizard that builds a complete personal system in Obsidian: vault structure, SQLite databases, Python data scripts, dynamic views, and GitHub backup.

**Commands:**

| Command | What It Does |
|---------|-------------|
| `/personal-os:setup` | Interactive wizard. Bootstrap a new vault or migrate an existing one. |
| `/personal-os:scan` | Scan any Obsidian vault and produce a structured discovery report. |

**Requirements:**
- Python 3.9+
- [Obsidian](https://obsidian.md)

[Read more →](plugins/personal-os/)

---

## Obsidian Skills

4 skills that make Claude fluent in Obsidian. Interactive skills have slash commands. Passive skills load automatically when you're editing the relevant file type.

| Skill | Type | What It Does |
|-------|------|-------------|
| `obsidian-cleanup` | Interactive | Vault health check: frontmatter, broken links, naming, bases. Run with `/obsidian-cleanup`. |
| `obsidian-markdown` | Passive | Teaches Claude wikilinks, embeds, callouts, properties, and tags. |
| `obsidian-bases` | Passive | Teaches Claude to create and edit `.base` files with views, filters, and formulas. |
| `obsidian-canvas` | Passive | Teaches Claude to create and edit `.canvas` files with nodes, edges, and groups. |

**Requirements:** None. These are pure markdown skills with no external dependencies.

[Read more →](skills/obsidian/)

---

## How Skills and Plugins Work

**Skills** are markdown files that teach Claude new capabilities. Put one in `~/.claude/skills/` and it loads automatically when relevant. No APIs, no config, no build step.

**Plugins** bundle multiple skills with templates and scripts. They use Claude Code's native plugin system and provide namespaced commands (e.g., `/personal-os:setup`).

<details>
<summary>Directory structure</summary>

```
claude-powerups/
├── skills/
│   ├── youtube-analyze/          # Standalone skill
│   │   ├── SKILL.md
│   │   └── assets/
│   │       └── youtube_transcripts.py
│   └── obsidian/                 # Skill collection
│       ├── obsidian-cleanup/
│       ├── obsidian-markdown/
│       ├── obsidian-bases/
│       └── obsidian-canvas/
└── plugins/
    └── personal-os/              # Plugin with skills + templates + scripts
        ├── skills/
        ├── templates/
        └── scripts/
```

</details>

## Contributing

Have an idea for a power-up? [Open an issue](https://github.com/Mykhailobabkin/claude-powerups/issues) or submit a PR.

## Credits

Built by [Mykhailo Babkin](https://x.com/babkin_ai) with Claude Code.

## License

MIT
