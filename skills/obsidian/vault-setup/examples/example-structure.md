# Example: Completed Vault Structure

This document shows what a fully set up knowledge base looks like after running the claude-memory-setup wizard. The example uses a fictional developer named Alex to illustrate a realistic vault.

---

## Meet Alex

Alex is a frontend developer at a startup called NovaTech. At work, Alex maintains two projects: a React Native **Mobile App** and an internal **Admin Dashboard**. Outside of work, Alex has two personal projects: a **Portfolio Site** and a **Budget Tracker** app. Alex runs three times a week, hits the gym twice a week, and is currently learning **Rust** and **System Design** in their spare time. Alex also takes meeting notes and tracks colleagues.

Here is what Alex's vault looks like after running the wizard.

---

## Full Folder Tree

```
MyVault/
├── Home.md
├── CLAUDE.md
├── Work Projects/
│   ├── Work Projects Dashboard.md
│   ├── Mobile App/
│   │   └── Mobile App.md
│   └── Admin Dashboard/
│       └── Admin Dashboard.md
├── Personal Projects/
│   ├── Personal Projects Dashboard.md
│   ├── Portfolio Site/
│   │   └── Portfolio Site.md
│   └── Budget Tracker/
│       └── Budget Tracker.md
├── Health & Training/
│   ├── Health & Training Dashboard.md
│   ├── Running/
│   │   ├── Running.md
│   │   └── January 15, 2026 - Running.md
│   └── Gym/
│       ├── Gym.md
│       └── January 16, 2026 - Gym.md
├── Learning/
│   ├── Learning Dashboard.md
│   ├── Rust/
│   │   └── Rust.md
│   └── System Design/
│       └── System Design.md
├── Meetings/
│   ├── Meetings.md
│   └── 2026-01-15 - Sprint Planning.md
└── People/
    ├── People.md
    ├── Sarah Chen.md
    └── Marco Rivera.md
```

The wizard created 22 files across 13 folders. Every file is connected to the others through backlinks, so clicking around in Obsidian's graph view reveals how everything relates.

---

## Trigger Phrases Table

This table lives inside `~/.claude/CLAUDE.md`. It tells Claude Code which vault files to read when Alex mentions specific topics in conversation.

| Trigger Phrases | Vault Location to Check |
|-----------------|-------------------------|
| "look in the vault", "check Obsidian", "in my vault" | Vault root -- read `CLAUDE.md` first, then navigate |
| "Mobile App", "work on Mobile App" | `Work Projects/Mobile App/Mobile App.md` |
| "Admin Dashboard", "work on Admin Dashboard" | `Work Projects/Admin Dashboard/Admin Dashboard.md` |
| "Portfolio Site", "portfolio" | `Personal Projects/Portfolio Site/Portfolio Site.md` |
| "Budget Tracker", "budget app" | `Personal Projects/Budget Tracker/Budget Tracker.md` |
| "training", "workout", "running", "gym" | `Health & Training/Health & Training Dashboard.md` |
| "learning", "studying", "Rust", "System Design" | `Learning/Learning Dashboard.md` |
| "meeting", "meeting notes" | `Meetings/Meetings.md` |
| "who is [name]", "people", "contacts" | `People/People.md` |

When Alex types "let's work on Mobile App" in any Claude Code conversation, Claude automatically reads `Mobile App.md` for context before responding.

---

## Sample Project File: Mobile App.md

This is what a project file looks like after Alex has been using the vault for a few weeks. The wizard creates it as a skeleton; Alex and Claude fill it in over time.

```markdown
# Mobile App

## Overview
NovaTech's customer-facing React Native app. Supports iOS and Android.
Handles user authentication, push notifications, and the core product
experience (browsing listings, making purchases, tracking orders).

Tech stack: React Native 0.76, TypeScript, Expo, Zustand for state
management, React Query for API calls.

Repo: github.com/novatech/mobile-app

## Current Status
- [x] Migrated from Redux to Zustand (completed Jan 10)
- [x] Push notification overhaul with Firebase Cloud Messaging
- [ ] Offline mode for browsing cached listings
- [ ] Accessibility audit (target: WCAG 2.1 AA)

## Key Decisions

| Date       | Decision                                | Reasoning                                                     |
|------------|-----------------------------------------|---------------------------------------------------------------|
| 2025-12-03 | Switch from Redux to Zustand            | Redux boilerplate was slowing down feature work. Zustand has 80% less code for the same result. |
| 2026-01-08 | Use Expo's EAS Build instead of Fastlane | Fastlane config was fragile. EAS handles both platforms with one config file. |
| 2026-01-14 | Defer deep linking to Q2                | Not enough user demand yet. Focus on offline mode first.      |

## Notes
- The listings API returns paginated results (50 per page). React Query's
  `useInfiniteQuery` handles this well -- see `src/hooks/useListings.ts`.
- Android builds take ~12 min on EAS, iOS takes ~18 min. Cache warming
  helps: run `eas build --clear-cache` only when native deps change.
- [[Sarah Chen]] owns the backend API. Coordinate with her on any
  schema changes.
- Related: [[2026-01-15 - Sprint Planning]] -- discussed offline mode scope.

---
<- [[Work Projects Dashboard]]
```

Notice how the file links to `[[Sarah Chen]]` (a person) and `[[2026-01-15 - Sprint Planning]]` (a meeting). These backlinks create a connected graph -- when Alex opens Sarah's file, they see every project and meeting she is mentioned in.

---

## Vault CLAUDE.md (Snippet)

This file lives at the root of the vault (`MyVault/CLAUDE.md`). It tells Claude how to navigate and update the vault. Here is a portion of it:

```markdown
# Knowledge Base -- Guide for Claude

## Vault Owner
Alex -- Frontend developer at NovaTech

## Critical Rule
When creating or modifying content in this vault:
- Update the relevant main file (project file, dashboard, hub)
- Add proper backlinks to related content using [[wiki-links]]
- Update any dashboards that track this content
- Keep cross-references consistent across the vault

## Vault Structure

MyVault/
|- Home.md
|- CLAUDE.md
|- Work Projects/
|   |- Work Projects Dashboard.md
|   |- Mobile App/
|   |   +- Mobile App.md
|   +- Admin Dashboard/
|       +- Admin Dashboard.md
|- Personal Projects/
|   |- Personal Projects Dashboard.md
|   |- Portfolio Site/
|   |   +- Portfolio Site.md
|   +- Budget Tracker/
|       +- Budget Tracker.md
|- Health & Training/
|   |- Health & Training Dashboard.md
|   |- Running/
|   |   +- Running.md
|   +- Gym/
|       +- Gym.md
|- Learning/
|   |- Learning Dashboard.md
|   |- Rust/
|   |   +- Rust.md
|   +- System Design/
|       +- System Design.md
|- Meetings/
|   +- Meetings.md
+- People/
    +- People.md

## How to Update Each Section

### Work Projects
When Alex mentions working on a project:
1. Read the project's main file first for context
2. After the session, update the project file with: what was accomplished,
   key decisions, next steps
3. If a new sub-document is needed, create it in the project's folder
   with a backlink to the project file
4. Update the dashboard if project status changed

### Health & Training
When Alex logs a training session:
1. Ask what activity type and session details
2. Create `[Date] - [Activity].md` in the correct activity folder
3. Add backlink to the activity hub: [[Activity Name]]
4. Update the Health & Training Dashboard progress log table with a new row
```

The full `CLAUDE.md` also includes naming conventions, linking rules, cross-reference tables, and instructions for every other section (Personal Projects, Learning, Meetings, People). The wizard generates all of this automatically based on the interview answers.

---

## How It All Connects

Here is what happens when Alex starts a new Claude Code conversation and types **"let's work on Mobile App"**:

1. Claude reads `~/.claude/CLAUDE.md` and finds the trigger phrase "Mobile App"
2. Claude navigates to `MyVault/Work Projects/Mobile App/Mobile App.md`
3. Claude reads the file and sees: the tech stack, current status, key decisions, and recent notes
4. Claude responds with full context -- no need for Alex to re-explain the project

Over time, the vault accumulates a searchable history of decisions, progress, and knowledge. It becomes a second brain that Claude can access instantly.

---

Your vault will look different -- the wizard customizes everything based on your answers. The sections, projects, activities, and trigger phrases are all generated from the interview in Phase 3. No two vaults are the same.
