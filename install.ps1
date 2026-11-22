<#
.SYNOPSIS
  Copy the write-in-your-voice skill into an agent's skill folder (Windows).
.EXAMPLE
  .\install.ps1                 (menu)
  .\install.ps1 -Agent cursor
  .\install.ps1 -Agent codex -Project C:\code\my-project
#>
param(
  [ValidateSet('', 'claude-code', 'codex', 'cursor', 'antigravity', 'all')]
  [string]$Agent = '',
  [string]$Project = ''
)
$ErrorActionPreference = 'Stop'
if (-not $Agent) {
  Write-Host 'Install the write-in-your-voice skill for:'
  Write-Host '  1) Claude Code'
  Write-Host '  2) ChatGPT desktop app / Codex'
  Write-Host '  3) Cursor'
  Write-Host '  4) Antigravity'
  Write-Host '  5) All of the above'
  $answer = Read-Host 'Number [5]'
  switch ($answer) {
    '1' { $Agent = 'claude-code' }
    '2' { $Agent = 'codex' }
    '3' { $Agent = 'cursor' }
    '4' { $Agent = 'antigravity' }
    ''  { $Agent = 'all' }
    '5' { $Agent = 'all' }
    default { throw "Unknown choice: $answer" }
  }
}
$Skill = 'write-in-your-voice'
$Src = Join-Path $PSScriptRoot "skills\$Skill"
if (-not (Test-Path (Join-Path $Src 'SKILL.md'))) { throw "Cannot find $Src\SKILL.md" }

function Get-TargetDir([string]$Name) {
  if ($Project) {
    switch ($Name) {
      'claude-code' { return Join-Path $Project '.claude\skills' }
      'codex'       { return Join-Path $Project '.agents\skills' }
      'cursor'      { return Join-Path $Project '.cursor\skills' }
      'antigravity' { return Join-Path $Project '.agents\skills' }
    }
  } else {
    switch ($Name) {
      'claude-code' { return Join-Path $HOME '.claude\skills' }
      'codex'       { return Join-Path $HOME '.agents\skills' }
      'cursor'      { return Join-Path $HOME '.cursor\skills' }
      'antigravity' { return Join-Path $HOME '.gemini\config\skills' }
    }
  }
}

function Install-One([string]$Name) {
  $Dir = Get-TargetDir $Name
  New-Item -ItemType Directory -Force -Path $Dir | Out-Null
  $Dest = Join-Path $Dir $Skill
  if (Test-Path $Dest) { Remove-Item -Recurse -Force $Dest }
  Copy-Item -Recurse -Path $Src -Destination $Dest
  Write-Host "${Name}: installed to $Dest"
}

if ($Agent -eq 'all') {
  foreach ($a in 'claude-code', 'codex', 'cursor', 'antigravity') { Install-One $a }
} else {
  Install-One $Agent
}
Write-Host 'Restart the agent so it rescans its skill folders.'
Write-Host 'For Claude on the web or desktop, upload release\write-in-your-voice.zip in Customize > Skills.'
