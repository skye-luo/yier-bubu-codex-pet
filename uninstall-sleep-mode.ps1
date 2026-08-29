[CmdletBinding()]
param(
    [string]$CodexHome = $(
        if ($env:CODEX_HOME) { $env:CODEX_HOME }
        else { Join-Path $HOME ".codex" }
    )
)

$ErrorActionPreference = "Stop"
$RuntimeRoot = Join-Path $CodexHome "yier-bubu-pet-sleep-mode"
$SchedulerPath = Join-Path $RuntimeRoot "pet_sleep_scheduler.ps1"
$TaskName = "YierBubuCodexPetSleep"
$UninstallStamp = Get-Date -Format "yyyyMMdd-HHmmss"
$BackupRoot = Join-Path $CodexHome "pets-backups\yier-bubu-sleep-uninstalled-$UninstallStamp"

if (Test-Path -LiteralPath $SchedulerPath -PathType Leaf) {
    & powershell.exe -NoProfile -NonInteractive -ExecutionPolicy Bypass -File $SchedulerPath -Mode Awake -CodexHome $CodexHome
}

& schtasks.exe /Delete /TN $TaskName /F 2>$null | Out-Null

if (Test-Path -LiteralPath $RuntimeRoot) {
    New-Item -ItemType Directory -Path $BackupRoot -Force | Out-Null
    Move-Item -LiteralPath $RuntimeRoot -Destination (Join-Path $BackupRoot "runtime")
}

Write-Host "睡眠定时已停用，一二和布布已恢复普通待机。"
if (Test-Path -LiteralPath $BackupRoot) {
    Write-Host "可恢复的定时组件位于：$BackupRoot"
}
