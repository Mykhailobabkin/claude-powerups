---
name: vault-setup
description: |
  Interactive wizard that sets up persistent memory for Claude Code using Obsidian + GitHub.
  Part of the Obsidian collection. Guides users through installing Obsidian, creating a
  personalized vault, backing it up to GitHub, and integrating it with Claude Code via CLAUDE.md
  trigger phrases. Use when the user mentions "knowledge base," "set up obsidian," "persistent
  memory," "vault setup," "obsidian claude," "claude memory," or invokes "/vault-setup."
---

## How This Skill Works

You are running an interactive setup wizard. Follow these rules:

1. **Go phase by phase** — never skip ahead unless the user explicitly asks
2. **Wait for "done"** at installation gates (Phases 1, 2, 5) — do not proceed until the user confirms
3. **Use AskUserQuestion** for all choices — do not just ask in text
4. **Use Write/Edit tools** to create files — do not just show the user what to write
5. **Store all Phase 3 responses** mentally — you will need them for Phases 4, 5, and 6
6. **NEVER overwrite ~/.claude/CLAUDE.md** — always Read it first, then use Edit to append
7. **Adapt verbosity** based on the Phase 0 experience level throughout the entire wizard
8. **Show progress** — at each phase, tell the user which step they are on (e.g., "Phase 3 of 7: Structure Interview")
9. **Be conversational** — this is a guided setup, not a wall of text. Keep each phase focused.
10. **Create directories** using Bash `mkdir -p` before writing files into them

---

## Phase 0: Experience Check

**Goal:** Determine verbosity level for the rest of the wizard.

Start with a brief welcome:

> **Welcome to the Claude Memory Setup Wizard.**
>
> This wizard will walk you through setting up a persistent knowledge base that Claude Code can access across all your conversations. By the end, you will have:
> - An organized Obsidian vault tailored to your life and projects
> - Automatic GitHub backup so nothing is ever lost
> - Claude Code integration so Claude checks your vault automatically when you mention your projects
>
> Let's start with a quick question.

Use **AskUserQuestion** to ask:

**Question:** "What's your experience level with Claude Code?"
**Type:** singleSelect
**Options:**
- **Beginner** — "I just installed Claude Code, or I'm new to it"
- **Experienced** — "I've been using Claude Code and know my way around"

Store the answer as `EXPERIENCE_LEVEL`.

- If **Beginner**: include explanations throughout (what Obsidian is, what CLAUDE.md does, why Git matters, what triggers are)
- If **Experienced**: skip explanations, just give actionable steps and move quickly

---

## Phase 1: Install Obsidian

**Progress: Phase 1 of 7 — Install Obsidian**

### If EXPERIENCE_LEVEL is Beginner:

Explain:

> **What is Obsidian?**
> Obsidian is a free note-taking app that stores everything as plain markdown files on your computer. Unlike Notion or Google Docs, your data never leaves your machine — it is just a folder of `.md` files. This makes it perfect for Claude Code, because Claude can read and write these files directly.
>
> Your "vault" is simply a folder. Everything inside it is your knowledge base.

### For everyone:

Tell the user:

> **Step 1:** Download and install Obsidian from https://obsidian.md (it's free).

Wait for the user to confirm they are done (tell them to type "done" when ready).

After confirmation, use **AskUserQuestion** to ask:

**Question:** "Where do you want your vault (your knowledge base folder)?"
**Type:** singleSelect
**Options:**
- `~/Documents/MyVault` — "Recommended. Easy to find, standard location."
- `~/Documents/KnowledgeBase` — "Alternative name if you prefer."
- **Other** — "I'll type a custom path."

If the user picks "Other", use a follow-up **AskUserQuestion** (type: text) to ask for the custom path.

Store the chosen path as `VAULT_PATH`.

Tell the user:

> **Step 2:** Open Obsidian and create a new vault:
> 1. Click "Create new vault"
> 2. Name it (e.g., "MyVault" or "KnowledgeBase")
> 3. Set the location to: `[VAULT_PATH]`
> 4. Click "Create"

Wait for the user to confirm they are done.

---

## Phase 2: Install GitHub CLI

**Progress: Phase 2 of 7 — GitHub Backup Setup**

### If EXPERIENCE_LEVEL is Beginner:

Explain:

> **Why GitHub?**
> Your vault lives on your computer, which means if something goes wrong, you could lose everything. GitHub gives you:
> - **Automatic backup** — your notes are saved to the cloud every few minutes
> - **Version history** — you can undo any change, even months later
> - **Sync across devices** — access your vault from any computer

### For everyone:

Detect the user's OS from the environment `platform` variable and give the appropriate install command:

- **macOS (darwin):** `brew install gh`
- **Linux:** `sudo apt install gh` (or direct them to https://cli.github.com for other distros)
- **Windows:** `winget install GitHub.cli`

Tell the user:

> 1. Install the GitHub CLI using the command above
> 2. Run `gh auth login` and follow the prompts to authenticate (choose GitHub.com, HTTPS, and browser login)

Wait for the user to confirm they are done.

---

## Phase 3: Structure Interview

**Progress: Phase 3 of 7 — Designing Your Knowledge Base**

Tell the user:

> Now I'll ask you a few questions to design your vault structure. This determines what folders, files, and templates I create — and what trigger phrases Claude will respond to.

### Question 1: Main Sections

Use **AskUserQuestion**:

**Question:** "What main sections do you want in your knowledge base? Pick all that apply."
**Type:** multiSelect
**Options:**
- **Work Projects** — "For work-related projects, tasks, and documentation"
- **Personal Projects** — "For personal projects, side hustles, hobbies"
- **Health & Training** — "For fitness tracking, health logs, workout routines"
- **Learning** — "For courses, tutorials, skills you're developing"
- **University/Education** — "For academic work, assignments, course notes"
- **Notes & Ideas** — "For general notes, journal entries, brainstorming"

Store as `SECTIONS`.

### Drill-Down Questions

For EACH selected section, ask a follow-up:

**If "Work Projects" selected:**

Use **AskUserQuestion** (type: text):
"What are your work projects? List their names separated by commas (e.g., 'Project Alpha, Client Dashboard, API Migration')."

Store as `WORK_PROJECTS` (split by comma, trim whitespace).

**If "Personal Projects" selected:**

Use **AskUserQuestion** (type: text):
"What personal projects are you working on? List their names separated by commas (e.g., 'My Blog, Recipe App, YouTube Channel')."

Store as `PERSONAL_PROJECTS`.

**If "Health & Training" selected:**

Use **AskUserQuestion** (type: multiSelect):
"What activities do you track?"
Options: Gym/Strength, Running, Swimming, Cycling, Yoga, Walking

Store as `ACTIVITIES`.

**If "Learning" selected:**

Use **AskUserQuestion** (type: text):
"What topics are you learning about? List them separated by commas (e.g., 'Python, Machine Learning, Design')."

Store as `LEARNING_TOPICS`.

**If "University/Education" selected:**

Use **AskUserQuestion** (type: text):
"What courses are you taking? List them separated by commas (e.g., 'CS 101, Math 200, English 102')."

Store as `COURSES`.

**If "Notes & Ideas" selected:**

No drill-down needed. This section gets a single folder with a dashboard.

### Additional Questions

Use **AskUserQuestion** (type: singleSelect) for each:

**Question:** "Do you want to track people (colleagues, contacts, friends) so Claude can cross-reference them in your notes?"
**Options:** Yes, No
Store as `TRACK_PEOPLE`.

**Question:** "Do you take meeting notes you'd like Claude to help organize and reference?"
**Options:** Yes, No
Store as `TRACK_MEETINGS`.

After all questions, confirm:

> Got it. Here's what I'll build for you:
> [List the sections, sub-items, and optional features the user chose]
>
> Creating your vault now...

---

## Phase 4: Build the Vault

**Progress: Phase 4 of 7 — Building Your Vault**

Use the **Bash** tool to create all directories with `mkdir -p`, then use the **Write** tool to create each file. Build everything in `VAULT_PATH`.

### 4a. Home.md

Create `[VAULT_PATH]/Home.md`:

```markdown
# Home

Welcome to your knowledge base. This is your persistent memory — everything here survives between conversations with Claude.

## Sections

[For each section the user chose, generate a wiki-link to its dashboard. Examples:]

- [[Work Projects Dashboard]] — Work-related projects and documentation
- [[Personal Projects Dashboard]] — Personal projects and side work
- [[Health & Training Dashboard]] — Fitness tracking and workout logs
- [[Learning Dashboard]] — Topics and skills in progress
- [[University Dashboard]] — Academic courses and assignments
- [[Notes & Ideas]] — General notes and brainstorming

[If TRACK_PEOPLE is Yes:]
- [[People]] — Contacts and colleagues directory

[If TRACK_MEETINGS is Yes:]
- [[Meetings]] — Meeting notes and action items
```

### 4b. Section Dashboards

For **each selected section**, create a folder and a dashboard file inside it.

**Work Projects** — Create `[VAULT_PATH]/Work Projects/Work Projects Dashboard.md`:

```markdown
# Work Projects

## Overview
Hub for all work-related projects. Claude reads this file when you mention any work project by name.

## Projects

[For each project in WORK_PROJECTS, generate:]
- [[PROJECT_NAME]] — [To be filled in]

---
<- [[Home]]
```

**Personal Projects** — Create `[VAULT_PATH]/Personal Projects/Personal Projects Dashboard.md`:

```markdown
# Personal Projects

## Overview
Hub for all personal projects. Claude reads this file when you mention any personal project by name.

## Projects

[For each project in PERSONAL_PROJECTS, generate:]
- [[PROJECT_NAME]] — [To be filled in]

---
<- [[Home]]
```

**Health & Training** — Create `[VAULT_PATH]/Health & Training/Health & Training Dashboard.md`:

```markdown
# Health & Training

## Overview
Hub for fitness tracking and training logs. Claude reads this file when you mention training, workouts, or specific activities.

## Activities

[For each activity in ACTIVITIES, generate:]
- [[ACTIVITY_NAME]] — Sessions and notes

## Progress Log

| Date | Session | Summary | Energy |
|------|---------|---------|--------|
| | | | |

---
<- [[Home]]
```

**Learning** — Create `[VAULT_PATH]/Learning/Learning Dashboard.md`:

```markdown
# Learning

## Overview
Hub for all topics and skills you are developing. Claude reads this file when you mention learning, studying, or specific topics.

## Topics

[For each topic in LEARNING_TOPICS, generate:]
- [[TOPIC_NAME]] — [To be filled in]

---
<- [[Home]]
```

**University/Education** — Create `[VAULT_PATH]/University/University Dashboard.md`:

```markdown
# University

## Overview
Hub for academic courses and assignments. Claude reads this file when you mention courses or university work.

## Courses

[For each course in COURSES, generate:]
- [[COURSE_NAME]] — [To be filled in]

---
<- [[Home]]
```

**Notes & Ideas** — Create `[VAULT_PATH]/Notes & Ideas/Notes & Ideas.md`:

```markdown
# Notes & Ideas

## Overview
A space for general notes, journal entries, and brainstorming. Anything that does not belong to a specific project lives here.

## Recent Notes

[Add notes here or let Claude create them as you work.]

---
<- [[Home]]
```

### 4c. Sub-Folders and Project/Topic Files

For each item within each section, create a subfolder and a main file.

**Work and Personal Projects** — For each project name, create:
- Directory: `[VAULT_PATH]/[Section]/[Project Name]/`
- File: `[VAULT_PATH]/[Section]/[Project Name]/[Project Name].md`

Template:

```markdown
# [Project Name]

## Overview
[Brief description — to be filled in]

## Current Status
- [ ] ...

## Key Decisions

| Date | Decision | Reasoning |
|------|----------|-----------|

## Notes
[Add notes as you work on this project. Claude will update this file when you ask.]

---
<- [[[Section] Dashboard]]
```

**Health Activities** — For each activity, create:
- Directory: `[VAULT_PATH]/Health & Training/[Activity Name]/`
- File: `[VAULT_PATH]/Health & Training/[Activity Name]/[Activity Name].md`

Template:

```markdown
# [Activity Name]

## Log
Sessions will appear here as you log them. Each session gets its own file in this folder.

## Goals
[What are you working toward?]

## Notes
[Techniques, programs, observations]

---
<- [[Health & Training Dashboard]]
```

**Learning Topics** — For each topic, create:
- Directory: `[VAULT_PATH]/Learning/[Topic Name]/`
- File: `[VAULT_PATH]/Learning/[Topic Name]/[Topic Name].md`

Template:

```markdown
# [Topic Name]

## Overview
[What are you learning and why?]

## Resources
- [ ] [Add courses, books, tutorials here]

## Notes
[Key concepts, insights, and progress]

---
<- [[Learning Dashboard]]
```

**University Courses** — For each course, create:
- Directory: `[VAULT_PATH]/University/[Course Name]/`
- File: `[VAULT_PATH]/University/[Course Name]/[Course Name].md`

Template:

```markdown
# [Course Name]

## Overview
[Course description — to be filled in]

## Progress

| Week | Assignment | Status |
|------|-----------|--------|
| | | |

## Notes
[Lecture notes, key concepts, study material]

---
<- [[University Dashboard]]
```

### 4d. People Folder (if TRACK_PEOPLE is Yes)

Create `[VAULT_PATH]/People/People.md`:

```markdown
# People

## Directory
Add people files here. Each person gets their own file. Backlinks will connect people to meetings, projects, and notes where they are mentioned.

### How to Add a Person
Create a file named `[Person Name].md` in this folder with:
- Role/relationship
- Context (which projects, teams)
- Any relevant notes

---
<- [[Home]]
```

### 4e. Meetings Folder (if TRACK_MEETINGS is Yes)

Create `[VAULT_PATH]/Meetings/Meetings.md`:

```markdown
# Meetings

## Meeting Notes
Meeting notes will appear here as backlinks. Each meeting gets its own file in this folder.

## Template
When logging a meeting, include:
- **Date** — when it happened
- **Attendees** — as [[Person Name]] links (if People tracking is enabled)
- **Key Decisions** — what was decided
- **Action Items** — who does what by when

## Recent Meetings

[Meeting files will be listed here as you create them.]

---
<- [[Home]]
```

### 4f. Vault CLAUDE.md

**This is the most critical file.** Create `[VAULT_PATH]/CLAUDE.md`:

Generate this file dynamically based on ALL data collected in Phase 3. The file must be specific to what the user chose — not a generic template.

```markdown
# Knowledge Base — Guide for Claude

## Vault Owner
[The user — they can personalize this later]

## Critical Rule
When creating or modifying content in this vault:
- Update the relevant main file (project file, dashboard, hub)
- Add proper backlinks to related content using [[wiki-links]]
- Update any dashboards that track this content
- Keep cross-references consistent across the vault

## Vault Structure

[Generate a tree showing the ACTUAL folder structure you just created. Example:]

```
[VAULT_NAME]/
|- Home.md
|- CLAUDE.md
|- Work Projects/
|   |- Work Projects Dashboard.md
|   |- [Project Name]/
|   |   +- [Project Name].md
|   +- [Project Name]/
|       +- [Project Name].md
|- Personal Projects/
|   |- Personal Projects Dashboard.md
|   +- ...
|- Health & Training/
|   |- Health & Training Dashboard.md
|   |- [Activity]/
|   |   +- [Activity].md
|   +- ...
[...continue for all sections created...]
```

## Naming Conventions
- Date format in filenames: `January 28, 2026` (human-readable, no leading zeros)
- Meeting notes: `YYYY-MM-DD - Meeting Name.md` (ISO date for sorting)
- General notes: `[Date] - [Description].md`

## Linking Rules

### Required Backlinks
Every file must link back to its hub/dashboard:

[Generate based on the sections that were created. Examples:]
- Work project files -> [[Work Projects Dashboard]]
- Personal project files -> [[Personal Projects Dashboard]]
- Health & Training sessions -> [[Activity Name]] hub
- Learning notes -> [[Learning Dashboard]]
- University assignments -> [[Course Name]] hub
- Meeting notes -> [[Meetings]]
- General notes -> [[Notes & Ideas]]

### Cross-Links
If content mentions something else in the vault, link it:

| If a file mentions... | Link to... |
|----------------------|------------|
[Generate rows based on sections. Examples:]
| A project by name | [[Project Name]] |
| A person | [[Person Name]] |
| A meeting | [[YYYY-MM-DD - Meeting Name]] |
| A training session | [[Date - Activity]] |
| A course | [[Course Name]] |

### The Graph Principle
If two pieces of content are connected in ANY way — link them. The goal: clicking any node in Obsidian's graph view shows everything related to it.

## How to Update Each Section

[Generate instructions for EACH section the user chose. Only include sections they selected.]

### Work Projects (if selected)
When the user mentions working on a project:
1. Read the project's main file first for context
2. After the session, update the project file with: what was accomplished, key decisions, next steps
3. If a new sub-document is needed, create it in the project's folder with a backlink to the project file
4. Update the dashboard if project status changed

### Personal Projects (if selected)
Same pattern as Work Projects.

### Health & Training (if selected)
When the user logs a training session:
1. Ask what activity type and session details
2. Create `[Date] - [Activity].md` in the correct activity folder
3. Add backlink to the activity hub: [[Activity Name]]
4. Update the Health & Training Dashboard progress log table with a new row

### Learning (if selected)
When the user learns something new:
1. Navigate to the relevant topic folder
2. Add notes to the topic's main file, or create a new sub-file for detailed notes
3. Add backlink to [[Learning Dashboard]]

### University (if selected)
When the user works on an assignment:
1. Read the course hub for context and progress
2. Create a `Week X/` folder if needed
3. Create the assignment file inside (e.g., `Week 3/Discussion.md`)
4. Add backlink to the course hub
5. Update the progress table in the course hub

### Notes & Ideas (if selected)
When the user wants to capture a note:
1. Create a new file in Notes & Ideas with a descriptive name
2. Add backlink to [[Notes & Ideas]]

### People (if enabled)
When a new person is mentioned:
1. Create `[Person Name].md` in the People folder
2. Add role, context, and how they relate to existing content
3. Link from relevant project/meeting files

### Meetings (if enabled)
When the user logs a meeting:
1. Create `YYYY-MM-DD - [Meeting Name].md` in the Meetings folder
2. Include: date, attendees (as [[Person]] links), key decisions, action items
3. Add backlink to [[Meetings]]
4. Cross-link to any projects or people discussed
```

After creating all files, tell the user:

> Your vault is built. I created [X] files across [Y] folders. Open Obsidian — you should see everything in the sidebar. Take a moment to explore the structure, then type "done" to continue.

Wait for "done".

---

## Phase 5: GitHub Backup

**Progress: Phase 5 of 7 — Setting Up GitHub Backup**

### 5a. Initialize Git

Run via **Bash** tool:

```bash
cd [VAULT_PATH] && git init
```

### 5b. Create .gitignore

Use **Write** tool to create `[VAULT_PATH]/.gitignore`:

```
.obsidian/workspace.json
.obsidian/workspace-mobile.json
.obsidian/graph.json
.obsidian/cache
.trash/
.DS_Store
```

### 5c. Create GitHub Repository

Use **AskUserQuestion** (type: text):

"What would you like to name your GitHub repository? (suggestion: 'knowledge-base')"

Store as `REPO_NAME`.

Run via **Bash** tool:

```bash
cd [VAULT_PATH] && git add -A && git commit -m "Initial vault setup" && gh repo create [REPO_NAME] --private --source=. --push
```

If the `gh repo create` command fails (e.g., repo name taken), tell the user and ask for a different name.

### 5d. Obsidian Git Plugin

Tell the user:

> Now let's set up automatic syncing so your vault backs up to GitHub every few minutes.
>
> **Install the Obsidian Git plugin:**
> 1. Open Obsidian
> 2. Go to Settings (gear icon, bottom-left)
> 3. Click "Community plugins" in the left sidebar
> 4. Click "Turn off Restricted Mode" if prompted (this is safe — it just enables community plugins)
> 5. Click "Browse" and search for **"Obsidian Git"**
> 6. Click "Install", then "Enable"
>
> **Configure it:**
> 1. Go to Settings -> Community plugins -> Obsidian Git (click the gear icon)
> 2. Set "Vault backup interval (minutes)" to **5**
> 3. Set "Auto pull interval (minutes)" to **5**
> 4. Set "Commit message on manual backup/auto backup" to: `vault backup: {{date}}`
> 5. Close settings
>
> Your vault will now automatically commit and push to GitHub every 5 minutes.

Wait for the user to confirm they are done.

---

## Phase 6: Claude Code Integration

**Progress: Phase 6 of 7 — Connecting Claude Code to Your Vault**

### If EXPERIENCE_LEVEL is Beginner:

Explain:

> **How Claude Code finds your vault:**
> Claude Code reads a file called `~/.claude/CLAUDE.md` at the start of every conversation. By adding "trigger phrases" to this file, you tell Claude: "When I mention these words, go check my vault for context."
>
> For example, if you have a project called "Recipe App" and you say "let's work on Recipe App" in any conversation, Claude will automatically open your vault and read the Recipe App project file before responding.

### For everyone:

**Step 1:** Use the **Read** tool to check if `~/.claude/CLAUDE.md` exists.

**Step 2:**

- **If the file EXISTS:** Read its full contents. Then use the **Edit** tool to APPEND the vault section below to the END of the file. NEVER overwrite existing content.
- **If the file DOES NOT EXIST:** Use the **Write** tool to create it with the vault section below.

**Vault section to add:**

Generate this dynamically from ALL Phase 3 data:

```markdown

## Obsidian Vault

**Location:** `[VAULT_PATH]`

### Auto-Check Triggers

When I mention any of these, check the Obsidian Vault first for context:

| Trigger Phrases | Vault Location to Check |
|-----------------|-------------------------|
| "look in the vault", "check Obsidian", "in my vault" | Vault root — read `CLAUDE.md` first, then navigate |
[For each Work Project:]
| "[PROJECT_NAME]", "work on [PROJECT_NAME]" | `Work Projects/[PROJECT_NAME]/[PROJECT_NAME].md` |
[For each Personal Project:]
| "[PROJECT_NAME]", "[PROJECT_NAME] project" | `Personal Projects/[PROJECT_NAME]/[PROJECT_NAME].md` |
[For each Health Activity:]
| "training", "workout", "[ACTIVITY_NAME]" | `Health & Training/Health & Training Dashboard.md` |
[For Learning:]
| "learning", "studying", "[TOPIC_NAME]" | `Learning/Learning Dashboard.md` |
[For University:]
| "university", "assignment", "[COURSE_NAME]" | `University/[COURSE_NAME]/[COURSE_NAME].md` |
[For Notes:]
| "notes", "ideas", "brainstorm" | `Notes & Ideas/Notes & Ideas.md` |
[If TRACK_PEOPLE:]
| "who is [name]", "people", "contacts" | `People/People.md` |
[If TRACK_MEETINGS:]
| "meeting", "meeting notes" | `Meetings/Meetings.md` |

### Vault Structure (Top-Level)

```
[VAULT_NAME]/
|- Home.md
|- CLAUDE.md
|- [Section folders...]
```

Always read the vault's `CLAUDE.md` for detailed navigation instructions and linking rules.

### How to Check the Vault
1. Read the vault's `CLAUDE.md` at `[VAULT_PATH]/CLAUDE.md`
2. Navigate to the relevant section based on the trigger
3. Read the main file before responding
```

**Step 3:** Tell the user:

> Claude Code is now connected to your vault. From now on, whenever you mention one of your trigger phrases in ANY Claude Code conversation, Claude will automatically check your vault for context before responding.

---

## Phase 7: Verification and Next Steps

**Progress: Phase 7 of 7 — Verification**

### 7a. Verify Setup

Tell the user:

> Your knowledge base is fully set up. Let's make sure everything works.
>
> **Quick test:**
> 1. Start a NEW Claude Code conversation (Cmd+N in the terminal, or open a new terminal tab)
> 2. Say: "[Pick one of the user's actual trigger phrases from Phase 6, e.g., 'Let's work on Project Alpha']"
> 3. Claude should read your vault and respond with context from the project file.

Ask the user if it worked. If not, troubleshoot:
- Check that `~/.claude/CLAUDE.md` exists and has the vault section
- Check that the vault path is correct and absolute
- Check that the trigger phrases are present in the file

### 7b. Quick-Reference Card

Print a summary card:

```
============================================
  YOUR KNOWLEDGE BASE — QUICK REFERENCE
============================================

  Vault Location:  [VAULT_PATH]
  GitHub Repo:     [REPO_NAME] (private)
  Auto-Backup:     Every 5 minutes via Obsidian Git

  TRIGGER PHRASES:
  ----------------------------------------
  [List every trigger phrase and what it opens, formatted as a clean table]

  Say any of these in a Claude Code conversation
  and Claude will check your vault automatically.

============================================
```

### 7c. Suggested Next Steps

Tell the user:

> **Your vault is live. Here's how to get the most out of it:**
>
> 1. **After each work session**, tell Claude: "Update the vault with what we accomplished today" — this keeps your project files current.
>
> 2. **Before starting work**, mention your project by name (e.g., "let's work on [one of their projects]") — Claude will read the latest state from your vault.
>
> 3. **Add new projects anytime** by creating a folder in the vault and adding a trigger phrase to `~/.claude/CLAUDE.md`.
>
> 4. **Your vault gets more valuable over time.** The more you use it, the more context Claude has about your work, decisions, and progress. Six months from now, you'll have a complete searchable history of everything you've built.
>
> Happy building. Your knowledge base is ready.
