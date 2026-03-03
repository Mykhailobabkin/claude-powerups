---
tags:
  - {{section_tag}}
  - hub
---

# {{section_name}}

{{section_overview}}

{{#if has_base_view}}
![[{{base_view_name}}.base]]
{{/if}}

{{#if sub_items}}
## {{sub_items_heading}}

{{#each sub_items}}
- [[{{this.name}}]] — {{this.description}}
{{/each}}
{{/if}}

{{#if related_sections}}
## Related

{{#each related_sections}}
- [[{{this}}]]
{{/each}}
{{/if}}

---
← [[Home]]
