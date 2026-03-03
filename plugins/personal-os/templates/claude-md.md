# {{vault_name}} — Guide for Claude

## Vault Location
`{{vault_path}}`

## Critical Rules
- Always read the relevant hub file before modifying section content
- Use [[wikilinks]] for all internal references
- Update hubs and dashboards when content changes
- Keep cross-references consistent

## Structure

```
{{vault_tree}}
```

## Sections

{{#each sections}}
### {{this.name}}
- **Hub:** [[{{this.hub_name}}]]
- **Purpose:** {{this.purpose}}
- **Data layer:** {{this.data_layer}}
{{#if this.frontmatter_schema}}
- **Frontmatter:**
  ```yaml
  {{this.frontmatter_schema}}
  ```
{{/if}}
{{/each}}

## Naming Conventions
{{#each naming_rules}}
- **{{this.directory}}:** `{{this.pattern}}`
{{/each}}

## Linking Rules

### Required Backlinks
Every file must link back to its hub:
{{#each sections}}
- Files in {{this.name}} → [[{{this.hub_name}}]]
{{/each}}

### Cross-Links
| If a file mentions... | Link to... |
|----------------------|------------|
{{#each cross_link_rules}}
| {{this.trigger}} | [[{{this.target}}]] |
{{/each}}

{{#if coder_mode}}
## Quick Commands
{{#each commands}}
| `{{this.command}}` | {{this.description}} |
{{/each}}
{{/if}}

{{#if task_board}}
## Task Board
- **Location:** {{task_board.folder}}
- **Task files:** Individual .md files with YAML frontmatter
- **Views:** {{task_board.views}}
- **Frontmatter schema:**
  ```yaml
  status: to-do    # {{task_board.status_values}}
  area: {{task_board.area_values}}
  type: {{task_board.type_values}}
  due: YYYY-MM-DD
  project: "Project Name"
  tags: [task]
  ```
{{/if}}
