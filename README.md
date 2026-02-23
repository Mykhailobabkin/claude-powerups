# Claude Power-Ups

**Skills that make Claude Code actually useful.** Each power-up is a plug-and-play skill that adds new capabilities to your Claude Code setup.

## Available Power-Ups

| Power-Up | What It Does | Command |
|----------|-------------|---------|
| [Claude Memory Setup](skills/claude-memory-setup/) | Interactive wizard that gives Claude persistent memory using Obsidian + GitHub. Claude remembers your projects, decisions, and progress across conversations. | `/claude-memory-setup` |

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
cp skills/claude-memory-setup/SKILL.md ~/.claude/skills/claude-memory-setup.md
```

## What Are Claude Code Skills?

Skills are markdown files that teach Claude new workflows. Drop a `.md` file into `~/.claude/skills/` and Claude gains a new capability — no plugins, no APIs, no config.

When you invoke a skill (e.g., `/claude-memory-setup`), Claude reads the file and follows the instructions inside. Skills can be interactive wizards, code generators, review checklists, or anything else you can describe in markdown.

## Coming Soon

More power-ups are in the works. Star the repo to get notified.

<!--
Ideas for future skills — uncomment as they're built:
- **Project Scaffolder** — Interactive project setup with best practices baked in
- **Code Review Buddy** — Structured code review with checklists and patterns
- **Debug Detective** — Systematic debugging workflow
-->

## Contributing

Have an idea for a power-up? [Open an issue](https://github.com/Mykhailobabkin/claude-powerups/issues) or submit a PR.

### Skill Structure

Each skill lives in its own folder under `skills/`:

```
skills/your-skill-name/
├── SKILL.md        ← The skill file (required)
├── README.md       ← Documentation (recommended)
└── examples/       ← Examples and references (optional)
```

## Credits

Built by [Misha Babkin](https://x.com/babkin_ai) with Claude Code.

## License

MIT
