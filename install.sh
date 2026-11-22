#!/usr/bin/env bash
# Copy the write-in-your-voice skill into an agent's skill folder.
#
#   ./install.sh <agent> [--project <dir>]
#
# <agent>: claude-code | codex | cursor | antigravity | all
# Run it with no arguments to choose from a menu.
# Without --project the skill is installed for the current user (all projects).
# With --project it is installed into that project or workspace only.
set -euo pipefail

SKILL=write-in-your-voice
SRC="$(cd "$(dirname "$0")" && pwd)/skills/$SKILL"
[ -f "$SRC/SKILL.md" ] || { echo "Cannot find $SRC/SKILL.md" >&2; exit 1; }

usage() { sed -n '2,9p' "$0" | sed 's/^# \{0,1\}//'; exit "${1:-0}"; }

choose_agent() {  # no arguments: ask which agent to install for
  echo "Install the write-in-your-voice skill for:"
  echo "  1) Claude Code"
  echo "  2) ChatGPT desktop app / Codex"
  echo "  3) Cursor"
  echo "  4) Antigravity"
  echo "  5) All of the above"
  printf "Number [5]: "
  read -r answer || answer=""
  case "${answer:-5}" in
    1) AGENT=claude-code ;; 2) AGENT=codex ;; 3) AGENT=cursor ;; 4) AGENT=antigravity ;;
    5) AGENT=all ;;
    *) echo "Unknown choice: $answer" >&2; exit 1 ;;
  esac
}

if [ $# -eq 0 ]; then choose_agent; else AGENT="$1"; shift; fi
PROJECT=""
while [ $# -gt 0 ]; do
  case "$1" in
    --project) [ $# -ge 2 ] || usage 1; PROJECT="$2"; shift 2 ;;
    -h|--help) usage 0 ;;
    *) echo "Unknown option: $1" >&2; usage 1 ;;
  esac
done

target_dir() {  # prints the skills directory for one agent
  if [ -n "$PROJECT" ]; then
    case "$1" in
      claude-code) echo "$PROJECT/.claude/skills" ;;
      codex)       echo "$PROJECT/.agents/skills" ;;
      cursor)      echo "$PROJECT/.cursor/skills" ;;
      antigravity) echo "$PROJECT/.agents/skills" ;;
    esac
  else
    case "$1" in
      claude-code) echo "$HOME/.claude/skills" ;;
      codex)       echo "$HOME/.agents/skills" ;;
      cursor)      echo "$HOME/.cursor/skills" ;;
      antigravity) echo "$HOME/.gemini/config/skills" ;;
    esac
  fi
}

install_one() {
  local dir; dir="$(target_dir "$1")"
  mkdir -p "$dir"
  rm -rf "${dir:?}/$SKILL"
  cp -R "$SRC" "$dir/$SKILL"
  echo "$1: installed to $dir/$SKILL"
}

case "$AGENT" in
  claude-code|codex|cursor|antigravity) install_one "$AGENT" ;;
  all) for a in claude-code codex cursor antigravity; do install_one "$a"; done ;;
  -h|--help) usage 0 ;;
  *) echo "Unknown agent: $AGENT" >&2; usage 1 ;;
esac
echo "Restart the agent so it rescans its skill folders."
echo "For Claude on the web or desktop, upload release/write-in-your-voice.zip in Customize > Skills."
