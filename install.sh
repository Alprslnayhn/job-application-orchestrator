#!/usr/bin/env bash
set -e

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BIN_TARGET_DIR="$HOME/.local/bin"
CONFIG_TARGET_DIR="$HOME/.config/job-orchestrator"

echo "======================================================"
echo "📦 Installing Job Application Orchestrator..."
echo "======================================================"

mkdir -p "$BIN_TARGET_DIR"
mkdir -p "$CONFIG_TARGET_DIR"

chmod +x "$REPO_DIR/src/job_orchestrator.py"
chmod +x "$REPO_DIR/bin/staj-basvur"

# Symlink executable commands to ~/.local/bin
ln -sf "$REPO_DIR/bin/staj-basvur" "$BIN_TARGET_DIR/staj-basvur"
ln -sf "$REPO_DIR/bin/staj-basvur" "$BIN_TARGET_DIR/basvur"
ln -sf "$REPO_DIR/bin/staj-basvur" "$BIN_TARGET_DIR/job-apply"

# Initialize default configuration if not already existing
if [ ! -f "$CONFIG_TARGET_DIR/config.json" ]; then
    cp "$REPO_DIR/config/config.example.json" "$CONFIG_TARGET_DIR/config.json"
    echo "✅ Created default configuration template at: $CONFIG_TARGET_DIR/config.json"
fi

echo "✅ Linked commands to $BIN_TARGET_DIR:"
echo "   - staj-basvur"
echo "   - basvur"
echo "   - job-apply"
echo ""
echo "Make sure $BIN_TARGET_DIR is in your PATH."
echo "Test installation with: job-apply --test"
echo "======================================================"
