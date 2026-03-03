---
tags:
  - home
aliases:
  - Dashboard
  - Start
---

# Home

> [!info] {{vault_description}}

## Sections

| Section | Description |
|---------|-------------|
{{#each sections}}
| [[{{this.hub_name}}]] | {{this.description}} |
{{/each}}

## Quick Links

{{#each quick_links}}
- [[{{this}}]]
{{/each}}

{{#if coder_mode}}
## Commands

| Command | What It Does |
|---------|-------------|
{{#each commands}}
| `{{this.command}}` | {{this.description}} |
{{/each}}
{{/if}}
