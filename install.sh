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

# Find all skills (any directory containing SKILL.md, at any depth)
INSTALLED=0
while IFS= read -r skill_file; do
    skill_dir=$(dirname "$skill_file")
    skill_name=$(basename "$skill_dir")

    cp "$skill_file" "$SKILLS_DIR/$skill_name.md"
    echo "  Installed: $skill_name"
    INSTALLED=$((INSTALLED + 1))
done < <(find "$REPO_DIR/skills" -name "SKILL.md" -type f | sort)

echo ""
if [ $INSTALLED -eq 0 ]; then
    echo "  No skills found to install."
    exit 1
fi

echo "  Done! $INSTALLED skill(s) installed to $SKILLS_DIR"
echo ""
echo "  Start a new Claude Code session to use them."
echo "  Run /vault-setup to set up persistent memory with Obsidian."
echo ""
