#!/bin/bash

# Claude Power-Ups Installer
# Installs Claude Code skills from this repo into ~/.claude/skills/

set -e

SKILLS_DIR="$HOME/.claude/skills"
REPO_DIR="$(cd "$(dirname "$0")" && pwd)"

echo ""
echo "  Claude Power-Ups Installer"
echo "  =========================="
echo ""

# Create skills directory if it doesn't exist
mkdir -p "$SKILLS_DIR"

# Find all skills (directories containing SKILL.md)
INSTALLED=0
for skill_dir in "$REPO_DIR"/skills/*/; do
    skill_name=$(basename "$skill_dir")
    skill_file="$skill_dir/SKILL.md"

    if [ -f "$skill_file" ]; then
        cp "$skill_file" "$SKILLS_DIR/$skill_name.md"
        echo "  Installed: $skill_name"
        INSTALLED=$((INSTALLED + 1))
    fi
done

echo ""
if [ $INSTALLED -eq 0 ]; then
    echo "  No skills found to install."
    exit 1
fi

echo "  Done! $INSTALLED skill(s) installed to $SKILLS_DIR"
echo ""
echo "  Start a new Claude Code session to use them."
echo "  Run /claude-memory-setup to set up persistent memory."
echo ""
