---
name: obsidian-cleanup
description: |
  Comprehensive vault health check with self-updating CLAUDE.md. Scans structure,
  audits frontmatter, checks links, validates naming, and syncs documentation to
  match reality. Works with any Obsidian vault — no hardcoded schemas or paths.
  Use when user mentions "vault cleanup", "vault health", "obsidian audit",
  "check my vault", or invokes "/obsidian-cleanup".
---

# Obsidian Vault Cleanup

An interactive vault audit that discovers your vault's structure and conventions, then checks everything against what it finds. Keeps your vault's CLAUDE.md in sync with reality — both before and after fixes.

## How This Skill Works

1. **Discovery-first.** Nothing is hardcoded. The skill scans your vault to learn its structure, frontmatter schemas, naming patterns, and installed plugins before checking anything.
2. **Two-pass CLAUDE.md sync.** Pre-cleanup (Phase 0) catches documentation drift. Post-cleanup (Phase 6) captures changes made by fixes.
3. **Phase-by-phase execution.** Run phases sequentially. Present findings after each phase. Ask before making changes.
4. **Severity-based fixes.** Critical issues get auto-fixed. Warning issues need confirmation. Info items are reported only.
5. **Use AskUserQuestion** for all user decisions — never assume.
6. **Use Write/Edit tools** for all file modifications — never show raw diffs and ask the user to apply them.
7. **Read before editing.** Always read a file with the Read tool before modifying it.
8. **Respect vault conventions.** Preserve existing annotation styles (← comments, etc.) when editing CLAUDE.md.

---

## Phase 0: Discovery & Pre-Cleanup CLAUDE.md Sync

**Goal:** Learn the vault's structure, infer its conventions, and update CLAUDE.md to match current reality — BEFORE running any audit phases.

### Step 0a: Locate the Vault

Find the vault root (the directory containing `.obsidian/`):

1. Check the current working directory for `.obsidian/`
2. If not found, check common locations:
   - `~/Documents/MyVault/`
   - `~/Documents/Obsidian/`
   - `~/Obsidian/`
   - `~/vault/`
3. If still not found, use AskUserQuestion: "Where is your Obsidian vault?"

Store the vault path for all subsequent phases.

### Step 0b: Scan Actual Structure

Build a complete picture of what exists:

- **Directories:** All folders, excluding `.obsidian/`, `.git/`, `.trash/`
- **Files by type:** `.md`, `.base`, `.canvas` — count and list by directory
- **Top-level layout:** Which major sections exist (by top-level folders)

Use Glob patterns: `**/*.md`, `**/*.base`, `**/*.canvas`. Use Bash `ls` for directory listing.

### Step 0c: Infer Frontmatter Schema

For each directory that contains content files:

1. Sample 2-3 `.md` files from the directory
2. Parse their YAML frontmatter (the `---` delimited block at the top)
3. Collect all keys and their observed values
4. Keys present in **80%+ of sibling files** = "expected" for that directory
5. Collect enum-like values (e.g., `status: to-do | in-progress | done`)

Build a schema map: `{ directory → { required_keys, optional_keys, enum_values } }`

**Heuristic for hub/index files** (skip these when computing "required"):
- File named after its parent folder (e.g., `Swimming.md` inside `Swimming/`)
- File named `Dashboard`, `Hub`, `Index`, `Home`, or `CLAUDE.md`
- `.base` and `.canvas` files (not markdown content)

### Step 0d: Detect Naming Patterns

For each directory, analyze filenames to detect:

- **Date formats:** `January 28, 2026`, `2026-01-28`, `Jan 28`, etc.
- **Separators:** ` - ` (space-dash-space), `_`, camelCase, kebab-case
- **Prefixes:** `Week X/`, date prefixes, type prefixes
- **Suffixes:** `Project.md`, `Changelog.md`, `Learnings.md`

Record the dominant pattern per directory. Flag files that deviate.

### Step 0e: Detect Installed Plugins

Read `.obsidian/plugins/` directory (if it exists):

| Plugin folder name | Feature it enables |
|---|---|
| `obsidian-kanban` | Kanban boards (Board.md files) |
| `obsidian-bases` or `make.md` | Base files (.base views) |
| `dataview` | Dataview queries |
| `obsidian-git` | Git auto-backup |
| `templater-obsidian` | Templates |

Record which plugins are active — this determines which checks run in Phase 4.

### Step 0f: Compare Against CLAUDE.md

If a `CLAUDE.md` exists at the vault root:

1. Read it fully
2. Parse it by heading sections
3. Compare each documentation section against discovered reality:

| CLAUDE.md Section | Compare Against |
|---|---|
| Structure tree (code block) | Actual directory tree from Step 0b |
| Frontmatter schemas | Inferred schemas from Step 0c |
| Naming conventions | Detected patterns from Step 0d |
| Linking rules | Observed link patterns in files |
| Plugin references | Detected plugins from Step 0e |

4. Build a diff report:
   - **Added:** Directories/files/keys that exist but aren't documented
   - **Removed:** Things documented but no longer present
   - **Changed:** Patterns that shifted (e.g., new enum values)

### Step 0g: Present Diff & Update

Present the diff report to the user. Use AskUserQuestion:
- "Update CLAUDE.md with these changes?" (Yes / Review each / Skip)

If **no CLAUDE.md exists**, generate one from the discovered data using the format from the vault-setup skill (structure tree, naming conventions, linking rules, frontmatter schemas).

If the user also has a **global `~/.claude/CLAUDE.md`** with vault trigger phrases, check if any triggers point to removed/renamed directories and flag them.

**After updating:** All subsequent phases use the now-accurate CLAUDE.md as their source of truth.

---

## Phase 1: Frontmatter Audit

**Goal:** Ensure content files have the frontmatter their siblings expect.

### What to Check

Using the schema map from Step 0c:

1. **Missing required keys:** File is in a directory where 80%+ of siblings have key X, but this file doesn't.
2. **Unexpected values:** Key has an enum pattern (e.g., `status` is always one of 5 values) but this file has an unrecognized value.
3. **Missing frontmatter entirely:** Content file (not a hub) has no YAML frontmatter block at all.
4. **Empty values:** Key exists but value is empty or null.

### What to Skip

- Hub/index files (detected in Step 0c heuristic)
- CLAUDE.md, lessons.md, README.md files
- Files in `.obsidian/`, `.git/`, `.trash/`

### Report Format

Group findings by directory:

```
## Frontmatter Issues

### Task Board/Tasks/ (3 issues)
- **Fix Upload Bug.md** — missing `scope` (present in 85% of siblings)
- **Research Auth.md** — `status: open` not in known values [to-do, in-progress, blocked, in-testing, done]
- **Quick Fix.md** — no frontmatter block

### Training Diary/Swimming/ (1 issue)
- **January 5, 2026 - Swimming.md** — missing `duration` (present in 90% of siblings)
```

---

## Phase 2: Naming Convention Audit

**Goal:** Find files that break their directory's naming pattern.

### What to Check

Using patterns from Step 0d:

1. **Date format inconsistency:** Files in the same directory use different date formats (e.g., one uses `January 5` and another uses `January 05`)
2. **Separator inconsistency:** Mix of ` - ` and `_` or other separators within the same directory
3. **Special characters:** Unusual characters that might cause issues (`:`, `?`, `*`, `|`, `<`, `>`, `"`)
4. **Double-prefixes:** Like `Week 3 - Week 3 - Discussion.md`
5. **Missing pattern elements:** Directory has a clear pattern (e.g., `[Date] - [Type].md`) and a file doesn't follow it

### Universal Checks (Always Apply)

These apply regardless of discovered patterns:

- No leading/trailing spaces in filenames
- No empty filenames
- No files with only an extension
- Consistent capitalization within the same directory (Title Case vs lowercase)

### Report Format

```
## Naming Issues

### Training Diary/Swimming/ — Pattern: "[Month Day, Year] - Swimming.md"
- **January 05, 2026 - Swimming.md** — Leading zero: should be "January 5, 2026"

### Meetings/ — Pattern: "YYYY-MM-DD - [Name].md"
- **team sync jan 15.md** — Doesn't match pattern: expected "2026-01-15 - Team Sync.md"
```

---

## Phase 3: Link Integrity Audit

**Goal:** Find broken links, orphaned files, and missing connections.

### 3a: Dead Wikilinks

Scan all `.md` files for `[[...]]` wikilinks. For each:

1. Extract the target (before `|` for display text, before `#` for heading links)
2. Check if a matching `.md` file exists anywhere in the vault
3. Check against YAML `aliases` in frontmatter (some files are found by alias, not filename)
4. Report links where no target file or alias match exists

### 3b: Orphaned Files

Find `.md` files that are NOT:
- Referenced by any wikilink from another file
- A hub/index file (Home.md, CLAUDE.md, Dashboard files, files named after their folder)
- Inside `.obsidian/`, `.git/`, `.trash/`
- A `.base` or `.canvas` file

### 3c: Cross-Link Completeness

Check logical connections. If the vault has patterns like:
- Task files → project references (if task mentions a project name, does it link to it?)
- Meeting notes → person links (if attendees are listed, are they wikilinked?)
- Session files → hub links (does a training session link back to its type hub?)

This phase uses the inferred schema to know what "type" of file it's looking at, then checks for expected link patterns within that type.

### Report Format

```
## Link Issues

### Dead Links (4 found)
- **Board.md** → `[[Old Task Name]]` — file doesn't exist
- **Meeting 2026-01-15.md** → `[[John]]` — no file or alias match

### Orphaned Files (2 found)
- **Learnings/old-draft.md** — not linked from anywhere
- **Tools/deprecated-script.md** — not linked from anywhere

### Missing Cross-Links (3 suggested)
- **Task: Fix Upload Bug.md** mentions "Video to Shorts" but doesn't link `[[Video to Shorts Project]]`
```

---

## Phase 4: Plugin-Specific Checks

**Goal:** Validate plugin-managed content. Only run checks for detected plugins (from Step 0e).

### If Kanban Plugin Detected

1. **Board ↔ file sync:** Every `[[Task]]` on a Kanban board must have a corresponding file. Every relevant file should appear on the board.
2. **Status consistency:** Card's Kanban column should match the file's `status:` frontmatter value.
3. **Done task cleanup:** Flag files with `status: done` that haven't been cleaned up (if vault conventions say done tasks get deleted).
4. **Overdue tasks:** Flag tasks where `due:` is in the past and `status:` is still `to-do`.

### If Bases Plugin Detected

1. **Valid syntax:** Each `.base` file should be parseable YAML
2. **Filter accuracy:** Check if filter conditions match files that actually exist
3. **Missing coverage:** Are there content files that should appear in a base view but don't (e.g., missing the required tag)?

### If Git Plugin Detected

1. **Gitignore coverage:** Check `.gitignore` covers common Obsidian exclusions:
   - `.obsidian/workspace.json`
   - `.obsidian/workspace-mobile.json`
   - `.obsidian/graph.json`
   - `.obsidian/cache/`
   - `.trash/`
   - `.DS_Store`
2. **Uncommitted changes:** Run `git status` to check for large numbers of uncommitted files

### Report Format

```
## Plugin Issues

### Kanban (Board.md)
- **Sync issue:** `[[Deploy Fix]]` on board but no file in Tasks/
- **Status mismatch:** `[[Auth Feature]]` in "Done" column but file has `status: in-progress`
- **Overdue:** `[[CSS Cleanup]]` due 2026-02-15, still `to-do`

### Bases
- **Missing tag:** `Training Diary/Swimming/Jan 5.md` has no `training` tag — won't appear in Training Dashboard.base

### Git
- **.gitignore missing:** `.obsidian/graph.json` not in .gitignore
```

---

## Phase 5: Summary & Fixes

**Goal:** Prioritize findings and apply fixes.

### Severity Classification

| Severity | Criteria | Action |
|----------|----------|--------|
| **Critical** | Breaks functionality: dead links, board sync issues, base query misses, missing frontmatter that hides files from views | Auto-fix after brief confirmation |
| **Warning** | Degrades quality: naming violations, missing project docs, overdue tasks, CLAUDE.md drift | Fix after explicit confirmation per item |
| **Info** | Optional improvements: orphaned files, suggested cross-links, empty directories | Report only — user decides |

### Present Summary

```
## Vault Health Report

### Critical (X issues) — will auto-fix
- [list]

### Warning (X issues) — confirm each
- [list]

### Info (X items) — for your review
- [list]
```

### Apply Fixes

Use AskUserQuestion: "Fix all Critical issues now?" (Yes / Review each first)

For Warning items, present each and ask: "Fix this?" (Yes / Skip / Fix all remaining)

When fixing:
- **Adding frontmatter:** Use Edit tool. Preserve existing file content. Add `---` block at top.
- **Renaming files:** Use Bash `mv`. Then Grep for old name across all files and update wikilinks.
- **Fixing links:** Use Edit tool. Replace broken `[[old]]` with correct `[[new]]`.
- **Adding links:** Use Edit tool. Insert wikilink at natural position in text.
- **Deleting files:** ALWAYS confirm with user first. Never delete without explicit approval.

---

## Phase 6: Post-Cleanup CLAUDE.md Sync

**Goal:** Update CLAUDE.md to reflect all changes made by Phases 1-5.

### When to Run

**Skip this phase entirely if Phases 1-5 made zero changes.**

### What to Do

1. **Re-scan the vault** (repeat Step 0b) to capture the current state after all fixes
2. **Diff against CLAUDE.md** — focus on sections that could have changed:
   - Structure tree → if files were renamed, moved, or deleted
   - Frontmatter schemas → if new keys were added to files
   - Naming conventions → if files were renamed to match patterns
   - Plugin references → if plugin state changed
3. **Update affected sections** using the Edit tool
4. If the user has a global `~/.claude/CLAUDE.md` with vault triggers, re-check triggers against the updated structure
5. Present what was updated

### Commit Changes

If the vault is a git repository:

```bash
cd [vault_path]
git add -A
git commit -m "vault cleanup: [brief summary of changes]"
```

Use AskUserQuestion before committing: "Commit all cleanup changes to git?" (Yes / No / Review diff first)

---

## Rules

- **Always read files before editing** — use the Read tool first
- **Never delete files without explicit confirmation** — even if they appear orphaned
- **When renaming files, update ALL wikilinks** that reference the old name
- **When adding frontmatter, preserve existing file content** — add the YAML block above, don't overwrite
- **Preserve existing CLAUDE.md style** — match annotation style (← comments), heading levels, and formatting
- **Be conversational** — explain what you found and why it matters, don't just dump lists
- **Show progress** — "Phase 2 of 6: Naming Conventions" at the start of each phase
