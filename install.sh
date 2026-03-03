#!/bin/bash

# Claude Power-Ups Installer
# Installs Claude Code skills and plugins from this repo

set -e

SKILLS_DIR="$HOME/.claude/skills"
REPO_DIR="$(cd "$(dirname "$0")" && pwd)"

echo ""
echo "  Claude Power-Ups Installer"
echo "  =========================="
echo ""

# Create skills directory if it doesn't exist
mkdir -p "$SKILLS_DIR"

# Find all skills (any directory containing SKILL.md, at any depth)
INSTALLED=0
while IFS= read -r skill_file; do
    skill_dir=$(dirname "$skill_file")
    skill_name=$(basename "$skill_dir")

    # Remove old flat-file install if it exists
    rm -f "$SKILLS_DIR/$skill_name.md"

    # Copy the full skill directory (preserves examples/, etc.)
    rm -rf "$SKILLS_DIR/$skill_name"
    cp -r "$skill_dir" "$SKILLS_DIR/$skill_name"

    # Remove README.md from installed copy (it's for GitHub, not for Claude)
    rm -f "$SKILLS_DIR/$skill_name/README.md"

    echo "  Installed: $skill_name"
    INSTALLED=$((INSTALLED + 1))
done < <(find "$REPO_DIR/skills" -name "SKILL.md" -type f | sort)

echo ""
if [ $INSTALLED -eq 0 ]; then
    echo "  No skills found."
fi

echo "  $INSTALLED skill(s) installed to $SKILLS_DIR"

# Detect plugins and show how to load them
PLUGINS_FOUND=0
PLUGIN_DIRS=""

if [ -d "$REPO_DIR/plugins" ]; then
    while IFS= read -r plugin_file; do
        plugin_dir=$(dirname "$(dirname "$plugin_file")")
        plugin_name=$(basename "$plugin_dir")
        PLUGIN_DIRS="$PLUGIN_DIRS --plugin-dir $plugin_dir"
        echo "  Found plugin: $plugin_name"
        PLUGINS_FOUND=$((PLUGINS_FOUND + 1))
    done < <(find "$REPO_DIR/plugins" -name "plugin.json" -path "*/.claude-plugin/*" -type f 2>/dev/null | sort)
fi

TOTAL=$((INSTALLED + PLUGINS_FOUND))
if [ $TOTAL -eq 0 ]; then
    echo "  Nothing found to install."
    exit 1
fi

echo ""
echo "  Done! $INSTALLED skill(s) installed."
echo ""
echo "  Start a new Claude Code session to use them."
echo "  Run /obsidian-cleanup to audit your vault."

if [ $PLUGINS_FOUND -gt 0 ]; then
    echo ""
    echo "  Plugins ($PLUGINS_FOUND found):"
    echo "  ─────────────────────────────────"
    echo "  Plugins use Claude Code's native plugin system."
    echo ""
    echo "  To load plugins for a session:"
    echo "    claude$PLUGIN_DIRS"
    echo ""
    echo "  Or to install permanently, set up a plugin marketplace."
    echo "  See: https://code.claude.com/docs/en/plugin-marketplaces"
fi
echo ""
