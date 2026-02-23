# Claude Memory Setup

**Give Claude Code persistent memory with an Obsidian knowledge base.**

A [Claude Code](https://docs.anthropic.com/en/docs/claude-code) skill that sets up a personal knowledge base Claude can read and write across every conversation.

---

## The Problem

Claude Code doesn't remember anything between conversations. Every new session starts from zero — no context about your projects, no memory of past decisions, no awareness of what you're working on.

## The Solution

This skill runs an interactive wizard that builds you a persistent knowledge base using [Obsidian](https://obsidian.md) (free, local-first markdown notes) and backs it up to GitHub. Claude walks you through the entire process step by step — from installing Obsidian to connecting everything to Claude Code.

Once set up, Claude automatically checks your vault whenever you mention one of your projects or trigger phrases. Say "let's work on my Recipe App" and Claude reads your project file before responding — picking up exactly where you left off, even in a brand new conversation.

## What You Get

- **A personalized Obsidian vault** structured around your actual projects, interests, and areas of life
- **Automatic GitHub backup** every 5 minutes via the Obsidian Git plugin
- **Claude Code integration** through trigger phrases in your `CLAUDE.md` — mention a project by name and Claude checks your vault automatically
- **Dashboard files** for each section (work, personal projects, learning, health, etc.)
- **Project templates** with status tracking, decision logs, and notes
- **Linking rules and conventions** so your vault stays organized as it grows
- **A vault `CLAUDE.md`** that teaches Claude how to navigate and update your knowledge base

## Prerequisites

- [Claude Code](https://docs.anthropic.com/en/docs/claude-code) installed and working
- A terminal (macOS, Linux, or Windows with WSL)
- A GitHub account (free is fine)

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
cp claude-powerups/skills/claude-memory-setup/SKILL.md ~/.claude/skills/claude-memory-setup.md
```

Then start a new Claude Code session and type `/claude-memory-setup` or say "set up my knowledge base".

## How It Works

The wizard runs in 7 phases:

| Phase | What Happens |
|-------|-------------|
| **1. Install Obsidian** | Download Obsidian and create your vault folder |
| **2. Install GitHub CLI** | Set up `gh` for automatic backup |
| **3. Structure Interview** | Claude asks about your projects, interests, and what you want to track |
| **4. Build the Vault** | Claude creates all folders, dashboards, project files, and the vault `CLAUDE.md` |
| **5. GitHub Backup** | Initialize git, create a private repo, configure auto-sync every 5 minutes |
| **6. Connect to Claude Code** | Add trigger phrases to `~/.claude/CLAUDE.md` so Claude checks your vault automatically |
| **7. Verify** | Test that everything works and get a quick-reference card |

The wizard adapts to your experience level. Beginners get full explanations of what Obsidian is, why Git matters, and how triggers work. Experienced users get straight to the point.

## Example Result

See [`examples/example-structure.md`](examples/example-structure.md) for what a completed vault looks like.

## FAQ

**Can I add more projects later?**
Yes. Create a new folder in your vault, add a project file, and add a trigger phrase to `~/.claude/CLAUDE.md`. Claude will pick it up in your next conversation.

**Does this work with an existing Obsidian vault?**
The wizard is designed for new vaults. If you have an existing vault, you can run the wizard with a new vault path and migrate content afterward.

**Is my data private?**
Your vault lives on your local machine. The GitHub repo is created as private by default. Nothing is sent anywhere except your own GitHub account.

**What if I don't use Obsidian?**
You can still browse and edit the vault files with any text editor — they are plain markdown. Obsidian just gives you a nice UI, graph view, and the auto-backup plugin.

## Credits

Created by [Misha Babkin](https://twitter.com/babkin_ai)

Built with [Claude Code](https://docs.anthropic.com/en/docs/claude-code)

## License

MIT
