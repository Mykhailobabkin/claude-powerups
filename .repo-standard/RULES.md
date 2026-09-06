# Shared development rules

These rules apply to every tool and model working in the Developer projects.
Repo CLAUDE.md contains the project-specific operating guide; read the relevant
section and the documents it points to. Read full lessons and history on demand.

## Quick development

1. Inspect the current code, repository status, and relevant guide before editing.
2. Work on a short-lived branch. Preserve unrelated edits and private local state.
3. Make the smallest complete change; run the tests relevant to its behaviour.
4. Add a brief CHANGELOG entry per completed code change. Update current docs
   only when behaviour, architecture, commands, configuration or operations changed.
5. Review the staged diff, run the repository check, commit explicit file paths,
   and merge through the repository's review process.

## Git and privacy

- Never use git add -A. Never stage a whole repository without reviewing every path.
- Never commit credentials, environment files, customer exports, caches or nested repositories.
- Use relative paths within repositories, ~/ in prose, and $HOME in shell code.
- Project goals and decisions belong in the project repository. Personal pay,
  career plans, relationship notes, negotiation strategy and private client quotes
  remain in private knowledge storage. Review histories and lessons too.
- Preserve private text before replacing a source note. A backup alone is not its
  working home. Mixed notes retain their private portions until private migration.
- Scope review to the actual repository audience, including public repositories.

## Documentation

- Every project has README.md, CLAUDE.md, CHANGELOG.md, docs/README.md and docs/project.md.
- CLAUDE.md has seven sections: Docs map, Architecture, Key Files,
  Patterns & Conventions, Deploy, Dev Commands, Gotchas. Aim for about 100 lines;
  preserve essential constraints and route detailed playbooks to docs/.
- Current facts live in current docs; dated plans in docs/superpowers are history.
- Lessons live in docs/lessons with a statement filename and short Gotcha pointer.
- Read skills/docs-standard for migration or setup; skills/changelog-discipline
  for changelog entries. Do not load either entire skill for unrelated work.
- AGENTS.md may be a generated tool adapter pointing to CLAUDE.md; never maintain
  a second competing guide. Team instructions must not depend on untracked rules.

## Enforcement

Run python3 .repo-standard/check.py from an installed repository. The same checker
runs in the local pre-commit hook and the docs-standard CI job. Local hooks are
convenience checks; required remote checks are the merge gate where supported.
Checks verify structure and obvious unsafe files; privacy and factual accuracy
still require reading the diff. Generated checker/adapters are updated from this
repo, not edited separately.
