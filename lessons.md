# Claude Powerups — Lessons Learned

## Mistakes and Rules

### 1. Claude Code HAS a native plugin system
**Mistake:** Initially said Claude Code doesn't have plugins and that we'd need to invent the mechanism.
**Rule:** Before saying a feature doesn't exist, always check the official docs first. The plugin system has existed since v1.0.33.

### 2. Everything must be universal
**Mistake:** Almost included references to Misha's specific vault structure (BRAIN, Body, Brand, etc.) in templates.
**Rule:** All templates, skills, and scripts must be 100% universal. No hardcoded user-specific content. Everything is discovered through interviews or scans.

### 3. Repo location matters
**Mistake:** Assumed the repo was in `~/Developer/claude-powerups`. It was actually cloned to `~/claude-powerups`.
**Rule:** Always verify file paths before assuming. Use `find` or `ls` to confirm.

### 4. vault-setup vs personal-os overlap
**Insight:** `/personal-os:setup` is a superset of the old `/vault-setup` skill. Keeping both would confuse users.
**Decision:** Retired vault-setup entirely. Added a note in the Obsidian skills README pointing users to the plugin.

### 5. README duplication during merge
**Mistake:** After the PR merge, the README had the Personal OS table duplicated (appeared twice).
**Rule:** After merging PRs, always re-read the merged file to check for duplicates or merge artifacts.
