<!-- Shared conventions: ~/.agents/AGENTS.md. Keep only project-specific facts here. -->
# Claude Powerups — Agent Guide

## Docs map

- [Project](docs/project.md): purpose, status and decisions.
- [Documentation index](docs/README.md): feature details and operations.
- [Changelog](CHANGELOG.md): changes and historical coverage.

## Architecture

Standalone skills live in skills/obsidian; plugins/personal-os bundles setup, scan, templates and scripts.

## Key Files

`install.sh`, `.claude-plugin/marketplace.json`, `plugins/personal-os/AGENTS.md`.

## Patterns & Conventions

Keep templates universal; discover user context through setup or scanning.

## Deploy

Users install via marketplace, local plugin loading or install.sh.

## Dev Commands

`bash -n install.sh` checks syntax. Installation changes local skills; run only when requested.

## Gotchas

- Keep Personal OS plugin-specific guidance in its nested AGENTS.md; do not recreate the retired vault-setup skill.
