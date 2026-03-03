---
name: personal-os:scan
description: |
  Scans an Obsidian vault and produces a structured discovery report. Identifies
  folder structure, frontmatter schemas, data domains (SQLite DBs, Python scripts),
  .base files, installed plugins, and CLAUDE.md/AGENT.md presence. Used standalone
  or by /personal-os:setup's migrate mode. Invoke with "/personal-os:scan" or
  "/personal-os:scan ~/path/to/vault".
---

# Vault Scanner

A read-only scanner that discovers everything about an Obsidian vault and produces a structured report. Works on any vault — no hardcoded paths, no assumptions about content.

## How This Skill Works

1. **Read-only.** Never create, modify, or delete any file in the vault. This is a pure discovery tool.
2. **Universal.** No hardcoded paths, folder names, or frontmatter keys. Everything is inferred from the vault itself.
3. **Use Bash for system commands** (`sqlite3`, `ls`, directory listing) and **Glob/Grep for file searches**.
4. **Present findings clearly** using tables, tree views, and structured markdown.
5. **Store or present the report** — write the final report directly in conversation output. If the scan was invoked by another skill (e.g., `/personal-os:setup`), return the structured data for downstream consumption.

---

## Phase 1: Locate Vault

**Goal:** Determine the vault root path.

Use this priority order — stop at the first match:

1. **Path argument from user.** If the user provided a path (e.g., `/personal-os:scan ~/my-vault`), expand `~` and use it. Verify it contains `.obsidian/` to confirm it is an Obsidian vault.
2. **Check `~/.claude/CLAUDE.md`.** Read the file and look for an `## Obsidian Vault` section. Extract the path from the `**Location:**` line.
3. **Check current working directory.** Use Bash to check if `.obsidian/` exists in the current working directory.
4. **Ask the user.** Use AskUserQuestion: "Where is your Obsidian vault? Provide the full path."

Once the vault path is confirmed, store it as `VAULT_PATH` and announce:

> **Vault located:** `[VAULT_PATH]`
> Starting scan...

---

## Phase 2: Structure Discovery

**Goal:** Map the vault's directory tree and count files by type.

### Step 2a: List Top-Level Directories

Use Bash `ls` on `VAULT_PATH` to list all top-level directories. **Exclude** these from the report:
- `.obsidian/`
- `.git/`
- `.trash/`
- `node_modules/`

Store the list as `TOP_LEVEL_DIRS`.

### Step 2b: Count Files by Type

For each top-level directory (and the vault root), use Glob to count files by extension:
- `.md` — Markdown notes
- `.base` — Obsidian Bases views
- `.canvas` — Canvas files
- `.py` — Python scripts
- `.db` / `.sqlite` — SQLite databases
- Other extensions — group as "other"

Also compute:
- Total file count across the vault (excluding `.obsidian/`, `.git/`, `.trash/`)
- Maximum nesting depth per top-level directory

### Step 2c: Build Tree View

Generate a tree representation of the top-level directories with file counts. Example:

```
BRAIN/
|- Home.md
|- CLAUDE.md
|- Work/                  (42 .md, 3 .base, 2 .py, 1 .db)
|  |- AIR/                (18 .md)
|  |- Creativeo/          (12 .md, 1 .py)
|  +- Tools/              (12 .md, 2 .py, 1 .db)
|- Brand/                 (25 .md, 4 .base, 3 .py)
|- Body/                  (15 .md, 1 .base, 2 .py, 1 .db)
+- Mind/                  (30 .md, 2 .base)
```

Only go two levels deep in the tree. Indicate deeper nesting with a note like "(3 levels deep)".

---

## Phase 3: Frontmatter Schema Detection

**Goal:** Discover what frontmatter keys each directory expects and what values they use.

### Step 3a: Sample Files

For each directory that contains `.md` files:

1. Identify all `.md` files in the directory (non-recursive — just that level).
2. **Skip hub/index files** when computing "required" keys. Hub files are:
   - Files named after their parent folder (e.g., `Swimming.md` inside `Swimming/`)
   - Files named `Dashboard`, `Hub`, `Index`, `Home`
   - `CLAUDE.md`, `README.md`, `AGENT.md`, `ForMisha.md`, `lessons.md`
3. Sample up to 5 content files (not hubs). If fewer than 3 content files exist, note the directory as "too few files for schema inference".
4. Parse the YAML frontmatter block (between `---` delimiters at the top of each file).

### Step 3b: Compute Schema

For each directory with enough samples:

1. Collect all frontmatter keys across sampled files.
2. **Expected keys:** Present in 80%+ of sampled sibling files.
3. **Optional keys:** Present in less than 80% of siblings.
4. **Enum-like values:** For each key, if there are fewer than 10 unique values across all sampled files, list them. These are likely enum fields (e.g., `status`, `type`, `area`).

### Step 3c: Record Schema Map

Build a schema map:

```
Directory: Task Board/Tasks/
  Expected keys: status, area, type, due, project, tags
  Optional keys: scope, clickup
  Enums:
    status: [to-do, in-progress, blocked, in-testing, done]
    area: [air, creativeo, personal, university, brand]
    type: [feature, bugfix, content, assignment, research, maintenance]
```

---

## Phase 4: Data Domain Detection

**Goal:** Find databases, scripts, and .base files — then map their relationships.

### Step 4a: SQLite Databases

Use Glob to find all `.db` and `.sqlite` files in the vault.

For each database found:
1. Note its location relative to the vault root.
2. Use Bash to list tables: `sqlite3 "[path]" ".tables"`
3. For each table, get the schema: `sqlite3 "[path]" ".schema [table_name]"` (limit to first 5 tables if there are many).
4. Note the row count: `sqlite3 "[path]" "SELECT COUNT(*) FROM [table_name];"` for each table.

### Step 4b: Python Scripts

Use Glob to find all `.py` files in the vault.

For each script:
1. Note its location.
2. Read the first 30 lines to understand its purpose.
3. Categorize it:
   - **Sync/fetch scripts** — pull data from external APIs (keywords: `requests`, `fetch`, `sync`, `pull`, `api`)
   - **Logger/tracker scripts** — write data to DBs or files (keywords: `insert`, `sqlite3`, `log`, `write`, `append`)
   - **Generator scripts** — produce content or output (keywords: `generate`, `create`, `render`, `template`)
   - **Init/setup scripts** — one-time setup (keywords: `init`, `setup`, `migrate`, `create_table`)
   - **Utility/other** — everything else

### Step 4c: Base Files

Use Glob to find all `.base` files in the vault.

For each `.base` file:
1. Note its location.
2. Read the file contents (they are YAML).
3. Parse the filters to understand what the base queries:
   - Which folders does it target? (`file.inFolder(...)`)
   - Which tags does it require? (`file.hasTag(...)`)
   - Which properties does it filter on? (`status == ...`, `area == ...`)
4. List the views defined (name and type).

### Step 4d: Map Relationships

Connect the dots:

| Relationship | How to Detect |
|---|---|
| Script writes to DB | Script imports `sqlite3` and references a `.db` file path |
| Script reads from API | Script imports `requests` or similar HTTP library |
| Base queries a directory | Base filter uses `file.inFolder("...")` |
| Base queries by tag | Base filter uses `file.hasTag("...")` |
| Base queries by property | Base filter uses property comparisons |

Present this as a data flow map:

```
[External API] --sync_script.py--> [data.db] --base_view.base--> [Obsidian View]
[Manual entry] --logger.py--> [training.db] --dashboard.base--> [Training Dashboard]
```

---

## Phase 5: Plugin Detection

**Goal:** Identify installed Obsidian plugins that affect vault behavior.

### Step 5a: Read Plugin Directory

Use Bash to list directories in `VAULT_PATH/.obsidian/plugins/` (if it exists).

Each subdirectory is an installed plugin. Record all of them.

### Step 5b: Flag Relevant Plugins

Highlight plugins that are architecturally significant:

| Plugin Folder Name | What It Enables |
|---|---|
| `obsidian-git` | Automatic git backup |
| `obsidian-kanban` | Kanban board files (`.md` with kanban metadata) |
| `obsidian-bases` or `make-md` | Base files (`.base` dynamic views) |
| `dataview` | Dataview queries in notes |
| `templater-obsidian` | Template system for new notes |
| `calendar` | Calendar view linked to daily notes |
| `obsidian-tasks` | Task management with query blocks |
| `obsidian-db-folder` | Database-like folder views |

Note any other plugins found, but do not flag them as significant unless they clearly affect vault structure.

---

## Phase 6: Documentation Check

**Goal:** Assess the vault's self-documentation state.

### Check for Key Files

| File | Location | Check |
|---|---|---|
| `CLAUDE.md` | Vault root | Exists? If yes, note its size and last modified date. Check if it references directories that no longer exist (stale). |
| `AGENT.md` | Vault root | Exists? If yes, note its purpose. |
| `.gitignore` | Vault root | Exists? If yes, check coverage (does it exclude `.obsidian/workspace.json`, `.trash/`, `.DS_Store`?). |
| Git repository | Vault root | Is `.git/` present? If yes, check for uncommitted changes count via `git status --porcelain`. |

### Staleness Check for CLAUDE.md

If `CLAUDE.md` exists, read it and compare its documented structure against the actual structure from Phase 2. Flag:
- **Documented but missing:** Directories or files mentioned in CLAUDE.md that do not exist.
- **Present but undocumented:** Top-level directories that exist but are not mentioned in CLAUDE.md.

---

## Phase 7: Output Report

**Goal:** Generate the final structured report.

Present the report directly in the conversation using this format:

```markdown
# Vault Scan Report

## Summary
- **Location:** [VAULT_PATH]
- **Total files:** X (.md: Y, .base: Z, .py: N, .db: M, other: O)
- **Top-level sections:** [comma-separated list of top-level directories]
- **Max nesting depth:** [deepest directory level found]
- **Git:** Yes (clean / X uncommitted changes) / No
- **CLAUDE.md:** Present (current / stale) / Missing
- **AGENT.md:** Present / Missing

## Structure

[Tree view from Phase 2, Step 2c]

## Frontmatter Schemas

[For each directory with a detected schema, render a block like:]

### [Directory Path]
| Key | Status | Observed Values |
|-----|--------|-----------------|
| status | Expected | to-do, in-progress, blocked, in-testing, done |
| area | Expected | air, creativeo, personal, university, brand |
| scope | Optional | (freeform text) |
| due | Expected | (date values) |

[If a directory has too few files for inference, note: "Too few files for schema inference (N files)"]

## Data Domains

[For each detected domain — group by the DB or data source:]

### [Domain Name] (e.g., "Training Data", "Brand Analytics")
- **Database:** [path relative to vault root] ([N] tables, [M] total rows)
- **Tables:** [list with row counts]
- **Scripts:** [list of .py files that interact with this DB]
- **Base views:** [list of .base files that query this domain's directory]
- **Data flow:** [External API] -> [script] -> [DB] -> [base view]

[If there are .base files not associated with a DB, list them separately:]

### Standalone Base Views
| Base File | Queries | View Types |
|-----------|---------|------------|
| Today.base | Task Board/Tasks/ (status, due) | table |
| Posts.base | Brand/Twitter/ (file.hasTag("post")) | table |

## Installed Plugins

| Plugin | Status | Significance |
|--------|--------|-------------|
| obsidian-git | Installed | Enables automatic git backup |
| obsidian-bases | Installed | Powers .base dynamic views |
| obsidian-kanban | Installed | Board-style task management |
| [other-plugin] | Installed | — |

## Documentation Status

| File | Status | Notes |
|------|--------|-------|
| CLAUDE.md | Present / Stale / Missing | [details] |
| AGENT.md | Present / Missing | [details] |
| .gitignore | Present / Missing | [coverage notes] |
| Git repo | Yes / No | [uncommitted changes count if applicable] |

## Recommendations

[Based on the decision tree below, provide specific recommendations for each top-level section of the vault.]
```

### Decision Tree for Recommendations

For each top-level section, evaluate which storage/view pattern fits:

**1. Recommend SQLite when:**
- The section contains timestamped numeric data logged regularly (e.g., training sessions with duration/distance/pace, analytics with daily metrics)
- Data has a clear tabular schema with consistent columns
- Scripts already exist that write to a DB, or the data volume suggests flat files will not scale
- Signal: `.db` or `.sqlite` already present, or `.py` scripts with `sqlite3` imports, or frontmatter with numeric fields logged over time

**2. Recommend Bases when:**
- The section contains notes with frontmatter properties that need dynamic filtering and grouping
- Users need views like "all tasks due this week" or "projects by status"
- The data is note-centric (each entry is a meaningful markdown document, not just a data row)
- Signal: `.base` files already present, or frontmatter with enum-like status/type fields, or Kanban boards

**3. Recommend plain markdown when:**
- The section is freeform narrative content (journals, meeting notes, brainstorming)
- Content does not have a consistent schema across files
- No need for dynamic filtering or aggregation
- Signal: files with little or no frontmatter, varied structures, prose-heavy content

**4. Cross-cutting recommendations:**
- If CLAUDE.md is missing: "Create a CLAUDE.md at the vault root to document structure and conventions for Claude Code."
- If CLAUDE.md is stale: "Update CLAUDE.md — it references directories/files that no longer exist."
- If no .gitignore: "Add a .gitignore to exclude Obsidian workspace files and system files."
- If no git: "Consider initializing a git repository for version history and backup."
- If there are Python scripts without a corresponding DB: "These scripts may benefit from writing to a central SQLite database instead of flat files."
- If there are .base files with filters that match zero files: "These base views may have stale filters — verify their query targets still exist."

Format each recommendation as:

```
### [Section Name]
**Current state:** [brief description of what exists]
**Recommendation:** [SQLite / Bases / Plain markdown / No change needed]
**Reasoning:** [1-2 sentences explaining why]
**Action:** [Specific next step if the user wants to act on it]
```

---

## Rules

1. **Never modify anything.** This skill is strictly read-only. Do not create, edit, or delete any file in the vault.
2. **No hardcoded assumptions.** Do not assume any folder names, frontmatter keys, or vault conventions. Discover everything from the vault itself.
3. **Graceful degradation.** If a phase cannot complete (e.g., no `.db` files found, no plugins directory), skip it cleanly and note "None found" in the report.
4. **Respect privacy.** Do not read or display the contents of files beyond what is needed for schema detection (frontmatter parsing, first 30 lines of scripts). Never dump full file contents into the report.
5. **Handle large vaults.** If a directory has more than 50 files, sample rather than exhaustively scan. Note the sample size in the report.
6. **Use parallel operations.** When scanning multiple directories or file types, use parallel Glob/Bash calls where possible to minimize latency.
7. **Structured for downstream use.** The report format is designed so that `/personal-os:setup` (migrate mode) can consume it programmatically. Keep the heading structure and table formats consistent.
