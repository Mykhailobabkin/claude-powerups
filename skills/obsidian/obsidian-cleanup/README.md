# Obsidian Cleanup

**Keep your vault healthy and your CLAUDE.md in sync with reality.**

A [Claude Code](https://docs.anthropic.com/en/docs/claude-code) skill that audits your Obsidian vault and automatically updates your documentation to match what actually exists. Part of the [Obsidian collection](../).

---

## The Problem

Obsidian vaults drift. You add new folders, rename files, introduce new frontmatter keys, install plugins — and your CLAUDE.md quietly goes stale. Claude keeps referencing a structure that no longer exists. Broken links accumulate. Files fall out of Base views because they're missing a tag. Nobody notices until something breaks.

## The Solution

This skill runs a comprehensive vault audit that **discovers your vault's conventions** rather than assuming them. It scans your actual files, infers your frontmatter schemas, detects your naming patterns, and compares everything against your CLAUDE.md documentation.

Two-pass CLAUDE.md sync: once **before** cleanup (to give the audit accurate context) and once **after** (to capture changes made by fixes). Your documentation stays in sync with your vault's reality, not the other way around.

## What It Checks

| Phase | What It Does |
|-------|-------------|
| **0. Discovery & CLAUDE.md Sync** | Scans vault structure, infers schemas, detects plugins, diffs against CLAUDE.md, updates docs |
| **1. Frontmatter Audit** | Finds files missing keys that 80%+ of their siblings have |
| **2. Naming Conventions** | Detects each directory's pattern, flags files that deviate |
| **3. Link Integrity** | Dead wikilinks (with alias resolution), orphaned files, missing cross-links |
| **4. Plugin-Specific Checks** | Kanban board sync, Base filter validation, gitignore coverage — only for detected plugins |
| **5. Summary & Fixes** | Prioritized report (Critical/Warning/Info), auto-fix with confirmation |
| **6. Post-Cleanup CLAUDE.md Sync** | Re-scans vault after fixes, updates CLAUDE.md to reflect final state |

## Key Feature: Self-Updating CLAUDE.md

Most vault tools check files but ignore documentation. This skill treats your `CLAUDE.md` as a living document:

- **Pre-cleanup:** Detects new folders, renamed files, changed schemas, and removed content that your CLAUDE.md doesn't reflect yet. Updates it before the audit runs, so all checks work against accurate docs.
- **Post-cleanup:** After fixes are applied (renamed files, added frontmatter, deleted stale content), re-diffs and updates CLAUDE.md again. You never have to manually sync your docs with your vault.

If no CLAUDE.md exists, the skill generates one from discovered data.

## Prerequisites

- [Claude Code](https://docs.anthropic.com/en/docs/claude-code) installed and working
- An Obsidian vault (any structure — the skill discovers yours)

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
cp claude-powerups/skills/obsidian/obsidian-cleanup/SKILL.md ~/.claude/skills/obsidian-cleanup.md
```

Then start a new Claude Code session and type `/obsidian-cleanup` or say "check my vault".

## Usage

```
/obsidian-cleanup
```

Claude will:
1. Find your vault (or ask for the path)
2. Scan and discover its structure
3. Compare against CLAUDE.md and offer updates
4. Run all audit phases
5. Present a prioritized health report
6. Fix issues with your confirmation
7. Sync CLAUDE.md with the final state

You can also say:
- "Run a vault health check"
- "Audit my Obsidian vault"
- "Check my vault for broken links"
- "Is my CLAUDE.md up to date?"

## Related Skills

- [vault-setup](../vault-setup/) — Create a new Obsidian vault from scratch with Claude Code integration
- [obsidian-markdown](../obsidian-markdown/) — Reference for Obsidian-flavored markdown syntax
- [obsidian-bases](../obsidian-bases/) — Reference for creating `.base` database views
- [obsidian-canvas](../obsidian-canvas/) — Reference for creating `.canvas` visual files

## Credits

Created by [Mykhailo Babkin](https://x.com/babkin_ai)

Built with [Claude Code](https://docs.anthropic.com/en/docs/claude-code)

## License

MIT
