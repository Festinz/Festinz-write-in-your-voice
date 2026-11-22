#!/usr/bin/env bash
# macOS: double-click this file in Finder to install the skill from a menu.
cd "$(dirname "$0")" || exit 1
./install.sh
echo
read -r -p "Press Enter to close this window. " _
