[CmdletBinding()]
param()

$ErrorActionPreference = "Stop"
$RepoRoot = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
$TaskName = "YierBubuCodexPetSleep"
$TestRoot = Join-Path ([IO.Path]::GetTempPath()) ("yier-bubu-win-test-" + [Guid]::NewGuid().ToString("N"))
$TestCodexHome = Join-Path $TestRoot ".codex"

try {
    $parseErrors = New-Object System.Collections.Generic.List[object]
    foreach ($script in Get-ChildItem -LiteralPath $RepoRoot -Filter *.ps1 -Recurse) {
        $tokens = $null
        $errors = $null
        [void][System.Management.Automation.Language.Parser]::ParseFile(
            $script.FullName,
            [ref]$tokens,
            [ref]$errors
        )
        foreach ($errorRecord in $errors) { $parseErrors.Add($errorRecord) }
    }
    if ($parseErrors.Count -gt 0) {
        throw "PowerShell 语法校验失败：`n$($parseErrors -join "`n")"
    }

    & (Join-Path $RepoRoot "verify.ps1")
    & (Join-Path $RepoRoot "install.ps1") -CodexHome $TestCodexHome

    foreach ($petId in @("yier", "bubu")) {
        $installedDir = Join-Path $TestCodexHome "pets\$petId"
        if (-not (Test-Path -LiteralPath (Join-Path $installedDir "pet.json"))) {
            throw "$petId 未正确安装 pet.json"
        }
        if (-not (Test-Path -LiteralPath (Join-Path $installedDir "spritesheet.webp"))) {
            throw "$petId 未正确安装 spritesheet.webp"
        }
    }

    & (Join-Path $RepoRoot "install-sleep-mode.ps1") -CodexHome $TestCodexHome
    & schtasks.exe /Query /TN $TaskName | Out-Null
    if ($LASTEXITCODE -ne 0) { throw "Windows 睡眠定时任务没有创建成功" }

    $scheduler = Join-Path $TestCodexHome "yier-bubu-pet-sleep-mode\pet_sleep_scheduler.ps1"
    & $scheduler -Mode Sleep -CodexHome $TestCodexHome
    foreach ($petId in @("yier", "bubu")) {
        $expected = (Get-FileHash -LiteralPath (Join-Path $RepoRoot "pets\$petId\spritesheet-night.webp") -Algorithm SHA256).Hash
        $actual = (Get-FileHash -LiteralPath (Join-Path $TestCodexHome "pets\$petId\spritesheet.webp") -Algorithm SHA256).Hash
        if ($expected -ne $actual) { throw "$petId 没有切换到夜间图集" }
    }

    & $scheduler -Mode Awake -CodexHome $TestCodexHome
    foreach ($petId in @("yier", "bubu")) {
        $expected = (Get-FileHash -LiteralPath (Join-Path $RepoRoot "pets\$petId\spritesheet.webp") -Algorithm SHA256).Hash
        $actual = (Get-FileHash -LiteralPath (Join-Path $TestCodexHome "pets\$petId\spritesheet.webp") -Algorithm SHA256).Hash
        if ($expected -ne $actual) { throw "$petId 没有恢复白天图集" }
    }

    & (Join-Path $RepoRoot "uninstall-sleep-mode.ps1") -CodexHome $TestCodexHome
    & (Join-Path $RepoRoot "uninstall.ps1") -CodexHome $TestCodexHome
    Write-Host "Windows 安装、定时切换与卸载流程通过。"
}
finally {
    $previousErrorAction = $ErrorActionPreference
    $ErrorActionPreference = "SilentlyContinue"
    & schtasks.exe /Delete /TN $TaskName /F 2>$null | Out-Null
    $ErrorActionPreference = $previousErrorAction
    if (Test-Path -LiteralPath $TestRoot) {
        Remove-Item -LiteralPath $TestRoot -Recurse -Force
    }
}
