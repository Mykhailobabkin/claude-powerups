---
name: personal-os:setup
description: |
  Interactive wizard that builds a Personal OS using Obsidian + SQLite + Python scripts.
  Two modes: bootstrap (create a new vault from scratch) or migrate (scan an existing vault,
  propose improvements, and execute approved changes). Generates folder structure, Home.md,
  section hubs, .base views, Python data scripts, CLAUDE.md, and GitHub backup.
  Use when the user mentions "personal os", "set up my vault", "build my system",
  "obsidian setup", "vault architect", or invokes "/personal-os:setup".
---

## How This Skill Works

You are running an interactive setup wizard that builds a complete Personal OS. Follow these rules:

1. **Go phase by phase** — never skip ahead unless the user explicitly asks
2. **Wait for confirmation** at key gates — do not proceed until the user approves
3. **Use AskUserQuestion** for all choices — do not just ask in text
4. **Use Write/Edit tools** to create files — do not show code and ask the user to copy it
5. **Store all interview responses** mentally — you will need them across all phases
6. **NEVER overwrite ~/.claude/CLAUDE.md** — always Read first, then use Edit to append
7. **Show progress** at each phase (e.g., "Phase 3 of 8: Data Layer Design")
8. **Be conversational** — this is a guided setup, not a wall of text
9. **Create directories** using Bash `mkdir -p` before writing files into them
10. **Everything is universal** — no hardcoded domains, platforms, or structures. All content comes from the user's answers.

### Template References

This skill uses templates from the plugin's `templates/` directory as patterns. You do NOT copy templates literally — you use them as structural guides and fill in content based on the user's interview answers. The templates show the shape of each file; you generate the actual content dynamically.

Similarly, script templates in `scripts/` show the pattern for Python data scripts. You generate real, working Python scripts based on these patterns, customized to the user's specific domains and schemas.

### Companion Skill References

When building vault files, follow syntax rules from the companion Obsidian skills if they are installed:

- **obsidian-markdown** — Obsidian-flavored markdown: `[[wikilinks]]`, YAML frontmatter, callout syntax, `#tags`
- **obsidian-bases** — `.base` file syntax for views, filters, formulas, and summaries
- **obsidian-canvas** — `.canvas` file syntax for visual layouts (if needed)

---

## Phase 0: Mode Selection

**Progress: Phase 0 of 8 — Getting Started**

Start with a welcome message:

> **Welcome to the Personal OS Setup Wizard.**
>
> This wizard will help you build a personal operating system — an Obsidian vault designed to manage your life, work, and projects. By the end, you'll have:
> - An organized vault with sections tailored to your life
> - A data layer (SQLite databases or Obsidian Bases) for anything you track regularly
> - Auto-generated Python scripts for logging and viewing your data (if you code)
> - GitHub backup so nothing is ever lost
> - Claude Code integration so Claude understands your system automatically

Use **AskUserQuestion** to ask:

**Question:** "Are you starting from scratch or do you have an existing Obsidian vault?"
**Options:**
- **Start fresh** — "I want to build a new vault from the ground up"
- **Migrate existing vault** — "I have an Obsidian vault I want to improve and restructure"

Store as `MODE` (bootstrap or migrate).

### If Migrate Mode

Tell the user:

> Great — I'll scan your existing vault first to understand what you have, then propose improvements. Nothing will be changed without your approval.

Run the `/personal-os:scan` skill (or perform the equivalent scan inline):
1. Ask for the vault path (or detect it)
2. Scan structure, frontmatter schemas, data domains, plugins
3. Store the scan report as `SCAN_REPORT`
4. Present a summary of findings

Then continue to Phase 1 with shorter interview questions (the scan fills in context).

### If Bootstrap Mode

Continue directly to Phase 1.

---

## Phase 1: Interview

**Progress: Phase 1 of 8 — Understanding Your Life**

Tell the user:

> Now I'll ask you a few questions to design your system. Your answers determine the folder structure, data layer, and automation I'll build.

### Question 1: Life Domains

Use **AskUserQuestion** (multiSelect):

**Question:** "What areas of your life do you want to manage? Pick all that apply."
**Options:**
- **Work / Career** — "Projects, clients, tasks, meetings, documentation"
- **Health / Fitness** — "Workouts, nutrition, sleep, habits, body metrics"
- **Learning / Education** — "Courses, topics, study notes, skill development"
- **Creative / Content** — "Writing, videos, music, art, social media, portfolio"
- **Finance / Business** — "Income, expenses, budgets, investments, invoices"
- **Personal / Life** — "Journal, goals, relationships, travel, hobbies"

Store as `DOMAINS`.

### Question 2: Data-Heavy Areas

Use **AskUserQuestion** (multiSelect):

**Question:** "Which of these involve data you track regularly — things with numbers, dates, and repeated entries?"
**Options:** (only show options matching selected DOMAINS)
- **Workout sessions** — "Reps, sets, duration, heart rate, distance"
- **Habits / Dailies** — "Did I do X today? Streaks, completion rates"
- **Analytics / Metrics** — "Views, followers, engagement, revenue numbers"
- **Finances** — "Transactions, income, expenses, recurring costs"
- **Health metrics** — "Weight, sleep hours, calories, body measurements"
- **Reading / Media log** — "Books read, articles, ratings, notes"

Store as `DATA_DOMAINS`.

### Question 3: Tools & Integrations

Use **AskUserQuestion** (multiSelect):

**Question:** "What external tools do you already use for tracking? (Helps me know what data sources exist)"
**Options:**
- **Fitness tracker** — "Whoop, Garmin, Apple Health, Fitbit, Strava"
- **Social media** — "YouTube, Twitter/X, TikTok, LinkedIn, Instagram"
- **Finance app** — "YNAB, Mint, spreadsheet, bank exports"
- **Project management** — "ClickUp, Notion, Linear, Jira, Trello"
- **None / Manual tracking** — "I track things manually or don't track yet"

Store as `TOOLS`. If specific tools are selected, ask a follow-up text question: "Which specific tools? (e.g., Whoop, YouTube, YNAB)"

### Question 4: Coder Level

Use **AskUserQuestion**:

**Question:** "Are you comfortable running Python scripts from the terminal?"
**Options:**
- **Yes — I code** — "Give me full Python scripts with SQLite databases"
- **A little — I can follow instructions** — "Give me scripts but explain how to run them"
- **No — keep it simple** — "Use Obsidian Bases only, no code required"

Store as `CODER_LEVEL` (coder / basic / no-code).

### Question 5: Drill-Down — Projects (if Work or Creative selected)

Use **AskUserQuestion** (text):

"What projects are you working on? List them separated by commas. Include both work and personal projects."

Store as `PROJECTS` (split by comma, trim whitespace).

### Question 6: Vault Location

Use **AskUserQuestion**:

**Question:** "Where should your vault live?"
**Options:**
- `~/Documents/PersonalOS` — "Recommended default location"
- `~/Documents/Vault` — "Simple and clean"
- **Other** — "I'll type a custom path"

Store as `VAULT_PATH`.

### Question 7: GitHub Backup

Use **AskUserQuestion**:

**Question:** "Do you want automatic GitHub backup?"
**Options:**
- **Yes** — "Private repo with auto-sync every 5 minutes"
- **Not now** — "I'll set this up later"

Store as `WANTS_GITHUB`.

### Migrate Mode Adjustments

If `MODE` is migrate:
- Skip Question 6 (vault path is known from scan)
- Skip Question 7 if scan detected git already initialized
- Pre-fill Question 1 from scan findings (which sections exist)
- Pre-fill Question 5 from scan findings (detected projects)
- Ask a confirmation question instead: "Based on the scan, here's what I found: [summary]. Does this look right, or would you like to add/remove anything?"

After all questions, confirm:

> Here's what I'll build:
>
> **Vault:** `[VAULT_PATH]`
> **Sections:** [list domains]
> **Data layer:** [for each DATA_DOMAIN, say whether it gets SQLite or Bases]
> **Projects:** [list]
> **GitHub:** Yes/No
>
> Ready to proceed?

Wait for confirmation.

---

## Phase 2: Architecture

**Progress: Phase 2 of 8 — Designing the Architecture**

### Data Layer Decision Tree

For each domain and data area the user selected, apply this decision tree to determine the right storage layer:

1. **Does this produce timestamped numeric data?** (workout logs, analytics, transactions) → **SQLite** (if coder) or **Bases with frontmatter** (if no-code)
2. **Is this data logged regularly?** (daily habits, weekly reviews) → **SQLite** or **Bases**
3. **Do you want aggregate views?** (trends, averages, totals) → **SQLite** (aggregation is natural in SQL)
4. **Is this mostly text with properties?** (tasks, projects, meeting notes) → **Bases** (.base views querying frontmatter)
5. **Is this freeform content?** (journal, notes, ideas) → **Plain markdown**

### Build the Blueprint

Create a mental blueprint mapping each domain to:

| Section | Folder Name | Data Layer | Hub File | Sub-folders |
|---------|-------------|------------|----------|-------------|
| (from DOMAINS) | (clean name) | SQLite / Bases / Markdown | (hub filename) | (from PROJECTS, etc.) |

Present this table to the user:

> Here's the architecture I'll build:
>
> [Table showing sections, data layers, and structure]
>
> **Key decisions:**
> - [Domain X] gets a SQLite database because you track numeric data regularly
> - [Domain Y] uses Bases views because it's structured notes with properties
> - [Domain Z] is plain markdown — freeform content that doesn't need querying

### Migrate Mode Adjustments

If `MODE` is migrate:
- Show a diff: what exists now vs. what the new architecture proposes
- For each proposed change, mark it as: **Add** (new), **Keep** (already exists), **Restructure** (move/rename), **New layer** (add SQLite/Bases to existing section)
- Use **AskUserQuestion** (multiSelect) to let the user approve/reject each change:
  "Which changes should I make?"
- Only proceed with approved changes

---

## Phase 3: Data Layer Design

**Progress: Phase 3 of 8 — Designing Your Data Layer**

**Skip this phase if no DATA_DOMAINS were selected or CODER_LEVEL is no-code.**

For each domain that gets a SQLite database, design the schema interactively:

### For Each Data Domain

Tell the user what you're designing:

> **Designing the [Domain Name] database.**
>
> Based on what you told me, here's the schema I'd suggest:

Present a proposed table with columns, types, and example data.

Use **AskUserQuestion** to confirm:

**Question:** "Does this schema capture what you want to track for [Domain Name]?"
**Options:**
- **Looks good** — "Use this schema"
- **Add columns** — "I want to track more things"
- **Simplify** — "Too many columns, keep it simpler"

If they want to add columns, ask a follow-up text question: "What else do you want to track? List the fields."

### Common Domain Schemas (Suggestions)

Use these as starting points — adapt to the user's specific answers:

**Fitness / Workouts:**
```
activity TEXT, duration_min INTEGER, distance_km REAL, heart_rate_avg INTEGER, notes TEXT
```

**Habits:**
```
habit TEXT, completed INTEGER (0/1), streak INTEGER, notes TEXT
```

**Finance:**
```
category TEXT, amount REAL, type TEXT (income/expense), description TEXT, recurring INTEGER (0/1)
```

**Analytics / Metrics:**
```
platform TEXT, metric TEXT, value REAL, notes TEXT
```

**Reading / Media:**
```
title TEXT, author TEXT, type TEXT (book/article/video), status TEXT (reading/done/dropped), rating INTEGER, notes TEXT
```

Store the final schemas as `SCHEMAS` — you'll use them in Phase 5.

---

## Phase 4: Build Vault Structure

**Progress: Phase 4 of 8 — Building Your Vault**

Use **Bash** `mkdir -p` and **Write** tool to create everything.

### 4a: Create Directories

For each section in the blueprint, create its directory tree:

```bash
mkdir -p "[VAULT_PATH]/[Section Name]"
```

For projects, create sub-directories:
```bash
mkdir -p "[VAULT_PATH]/[Section Name]/[Project Name]"
```

If the user has data domains with SQLite, create a scripts directory:
```bash
mkdir -p "[VAULT_PATH]/scripts"
```

If a task board is needed:
```bash
mkdir -p "[VAULT_PATH]/Task Board/Tasks"
```

### 4b: Create Home.md

Create `[VAULT_PATH]/Home.md` based on the `templates/home.md` pattern.

Fill in:
- `{{vault_description}}` — A one-liner based on the user's domains (e.g., "Your personal operating system — managing work, health, and learning.")
- `{{sections}}` — One row per section with wikilink to hub and description
- `{{quick_links}}` — Links to most important hubs
- `{{commands}}` — If coder mode, list the Python scripts that will be created

### 4c: Create Section Hubs

For each section, create a hub file: `[VAULT_PATH]/[Section]/[Section Name].md`

Based on `templates/hub.md` pattern. Fill in:
- Section name, tag, overview text
- Sub-items list (projects, topics, activities — whatever belongs in this section)
- Related sections (other sections that connect to this one)
- Base view embed if the section will have a .base file

### 4d: Create Project/Item Files

For each project or sub-item within a section, create its file:
- `[VAULT_PATH]/[Section]/[Project Name]/[Project Name].md`

With sections: Overview, Current Status, Key Decisions table, Notes, and backlink to hub.

### 4e: Create Task Board (if applicable)

If the user selected Work or has projects, create a task board:

1. Create `Task Board/Tasks/` directory
2. Create `Task Board/Today.base` — filters for in-progress + due today + overdue tasks
3. Create `Task Board/Backlog.base` — all tasks grouped by area
4. Create a sample task file in `Task Board/Tasks/` to demonstrate the format

Base files follow the `templates/base-view.base` pattern. Task files follow `templates/task-file.md`.

### 4f: Create .gitignore

Copy `templates/gitignore.txt` content to `[VAULT_PATH]/.gitignore`.

### Migrate Mode Adjustments

If `MODE` is migrate:
- Only create directories and files that were approved in Phase 2
- Never overwrite existing files — check with Read tool first
- For restructured sections, create new structure alongside old, then prompt user to confirm the move

After creating all files, tell the user:

> Vault structure is built. I created [X] files across [Y] folders. Take a look in Obsidian, then tell me when you're ready to continue.

Wait for confirmation.

---

## Phase 5: Build Data Layer

**Progress: Phase 5 of 8 — Building the Data Layer**

### If CODER_LEVEL is coder or basic

For each DATA_DOMAIN that gets SQLite:

#### Generate init script
Based on `scripts/init_db.py.tmpl` pattern, create a real Python script:
- File: `[VAULT_PATH]/scripts/init_[domain_slug]_db.py`
- Fill in the actual table name, columns from the schema designed in Phase 3
- Include any seed data if relevant

#### Generate logger script
Based on `scripts/log_entry.py.tmpl` pattern:
- File: `[VAULT_PATH]/scripts/log_[domain_slug].py`
- CLI args matching the schema columns
- Date defaults to today

#### Generate overview generator
Based on `scripts/generate_overview.py.tmpl` pattern:
- File: `[VAULT_PATH]/scripts/generate_[domain_slug].py`
- Queries for summary stats, recent entries, and trends
- Writes markdown overview to the section's directory

#### Generate orchestrator
Based on `scripts/update_all.py.tmpl` pattern:
- File: `[VAULT_PATH]/scripts/update_all.py`
- Imports and runs all generate_* scripts

#### Initialize databases
Run each init script:
```bash
cd [VAULT_PATH]/scripts && python3 init_[domain_slug]_db.py
```

### If CODER_LEVEL is no-code

Skip Python scripts entirely. Instead, create additional .base files:

For each DATA_DOMAIN:
- Create a `.base` file that queries files with the domain's tag
- Design frontmatter schemas that capture the same data points
- Create a sample entry file showing the frontmatter format
- The user logs entries by creating new .md files with frontmatter (Obsidian makes this easy with templates)

### Create .base Views for All Sections

Regardless of coder level, create `.base` views for sections that benefit from dynamic views:
- Task boards (always)
- Any section with structured data (projects with status, items with dates)
- Habit trackers (if selected)

Each `.base` file follows the `templates/base-view.base` pattern.

After building, tell the user:

> Data layer is set up. [Summary of what was created — scripts, databases, base views].

If coder mode, show them how to use the scripts:
```
python3 scripts/log_[domain].py --[arg] value
python3 scripts/update_all.py
```

---

## Phase 6: Build Companion Files

**Progress: Phase 6 of 8 — Documentation & Integration**

### 6a: Vault CLAUDE.md

Create `[VAULT_PATH]/CLAUDE.md` — **this is the most critical file.**

Based on `templates/claude-md.md` pattern, generate a vault-specific CLAUDE.md that includes:

1. **Vault location** — absolute path
2. **Structure tree** — actual tree of what was just created
3. **Sections** — for each section: hub file, purpose, data layer, frontmatter schema
4. **Naming conventions** — per directory (e.g., task files, session logs, meeting notes)
5. **Linking rules** — required backlinks and cross-link rules
6. **Quick commands** — if coder mode, list all Python scripts with usage
7. **Task board schema** — if task board was created
8. **How to update each section** — section-specific instructions for Claude

This file must be **specific to what was actually built**, not a generic template.

### 6b: AGENT.md (Optional)

If the vault has multiple sections and the user is a coder, create an AGENT.md with:
- Naming conventions for each directory
- How agents should handle concurrent edits (scope-based)
- File creation patterns per section

### 6c: Update ~/.claude/CLAUDE.md

**CRITICAL: Read the file first, then append.**

1. Use **Read** to check if `~/.claude/CLAUDE.md` exists
2. If it exists, use **Edit** to append the vault integration section
3. If it doesn't exist, use **Write** to create it with the vault section

The vault section to append:

```markdown

## Obsidian Vault

**Location:** `[VAULT_PATH]`

### Auto-Check Triggers

When I mention any of these, check the Obsidian Vault first:

| Trigger Phrases | Vault Location to Check |
|-----------------|-------------------------|
| "look in the vault", "check Obsidian", "in my vault" | Vault root — read `CLAUDE.md` first |
[For each section, generate trigger phrases and paths]
[For each project, generate project-specific triggers]

### Vault Structure (Top-Level)
```
[Actual tree]
```

Always read the vault's `CLAUDE.md` for detailed navigation instructions.
```

---

## Phase 7: Git & GitHub Setup

**Progress: Phase 7 of 8 — Backup & Version Control**

**Skip if WANTS_GITHUB is "Not now".**

### 7a: Initialize Git

```bash
cd [VAULT_PATH] && git init
```

### 7b: Initial Commit

```bash
cd [VAULT_PATH] && git add -A && git commit -m "Initial Personal OS setup"
```

### 7c: Create GitHub Repository

Use **AskUserQuestion** (text):
"What would you like to name your GitHub repository? (suggestion: 'personal-os')"

Store as `REPO_NAME`.

```bash
cd [VAULT_PATH] && gh repo create [REPO_NAME] --private --source=. --push
```

If the command fails (repo name taken), tell the user and ask for a different name.

### 7d: Obsidian Git Plugin

Tell the user how to install and configure the Obsidian Git plugin:

> **Set up automatic syncing:**
> 1. In Obsidian → Settings → Community plugins → Browse
> 2. Search for "Obsidian Git" → Install → Enable
> 3. Configure: backup interval = 5 min, auto pull = 5 min
> 4. Commit message: `vault backup: {{date}}`
>
> Your vault will auto-sync to GitHub every 5 minutes.

Wait for confirmation.

---

## Phase 8: Verification

**Progress: Phase 8 of 8 — Verification**

### 8a: Run Scan

Run `/personal-os:scan` on the newly created vault to verify:
- All directories exist
- All files have correct frontmatter
- Base files have valid YAML
- Scripts run without errors (if coder mode)
- CLAUDE.md matches actual structure
- Git is properly initialized (if GitHub was set up)

Present any issues found and fix them.

### 8b: Quick Reference Card

Print a summary:

```
============================================
  YOUR PERSONAL OS — QUICK REFERENCE
============================================

  Vault:     [VAULT_PATH]
  Sections:  [list]
  Data:      [X SQLite databases, Y .base views]
  GitHub:    [repo name] (private)
  Backup:    Every 5 minutes via Obsidian Git

  SECTIONS:
  ─────────────────────────────────
  [For each section: name, hub file, data layer]

  COMMANDS: (if coder mode)
  ─────────────────────────────────
  [For each script: command and what it does]

  TRIGGER PHRASES:
  ─────────────────────────────────
  [List trigger phrases that activate vault context]

============================================
```

### 8c: Next Steps

> **Your Personal OS is live. Here's how to get the most out of it:**
>
> 1. **Open Obsidian** and explore the structure. Your Home.md is the starting point.
> 2. **Mention your projects by name** in Claude Code conversations — Claude will read your vault automatically.
> 3. **After each work session**, tell Claude: "Update the vault with what we did today."
> [If coder mode:]
> 4. **Log data entries** with the scripts: `python3 scripts/log_[domain].py --help`
> 5. **Regenerate overviews** anytime: `python3 scripts/update_all.py`
> [If task board:]
> 6. **Create tasks** by adding .md files to `Task Board/Tasks/` with the frontmatter template.
>
> Your system gets more valuable over time. The more you use it, the more context Claude has. Six months from now, you'll have a complete searchable history of everything you've built.

---

## Rules Summary

- **Universal** — No hardcoded domains, platforms, or structures. Everything comes from the user's answers.
- **Non-destructive** — In migrate mode, never delete or overwrite without explicit approval.
- **Real scripts** — Generate working Python scripts, not templates. Test them after creation.
- **Adaptive** — Coder gets SQLite + scripts. Non-coder gets Bases + frontmatter. Both get a fully functional system.
- **Companion skills** — Use obsidian-markdown, obsidian-bases, and obsidian-canvas syntax rules if installed.
- **Decision tree** — Always apply the data layer decision tree: timestamped numbers → SQLite, structured notes → Bases, freeform → markdown.
