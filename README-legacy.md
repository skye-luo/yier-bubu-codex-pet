# 一二 × 布布：Codex 宠物

一个只包含“一二”和“布布”的独立 Codex Desktop 宠物项目。两个角色都保留完整工作动画，并会在每天 22:00–次日 08:00 自动进入夜间待机：没有任务时睡觉，工作、等待确认或检查时保持原动作。

> 非官方、非商业的粉丝体验版本。角色素材不在 MIT 许可范围内，详见 [ASSET-NOTICE.md](ASSET-NOTICE.md)。

## 预览

| 一二 | 布布 |
| --- | --- |
| ![一二待机动画](docs/previews/yier-idle.gif) | ![布布待机动画](docs/previews/bubu-idle.gif) |

| 一二夜间待机 | 布布夜间待机 |
| --- | --- |
| ![一二睡眠动画](docs/previews/yier-sleep.gif) | ![布布睡眠动画](docs/previews/bubu-sleep.gif) |

- [一二完整动作表](docs/yier-contact-sheet.png)
- [布布完整动作表](docs/bubu-contact-sheet.png)
- [一二夜间动作表：仅待机行睡觉](docs/yier-sleep-contact-sheet.png)
- [布布夜间动作表：仅待机行睡觉](docs/bubu-sleep-contact-sheet.png)

## 一行安装

### Windows

打开 PowerShell，复制这一行（不需要提前安装 Git）：

```powershell
irm https://raw.githubusercontent.com/skye-luo/yier-bubu-codex-pet/v1.1.0/quick-install.ps1 | iex
```

这条命令会：

- 将“一二”和“布布”安装到 `%USERPROFILE%\.codex\pets`；
- 注册一个当前用户的 Windows 定时任务，每 5 分钟校正一次本地时间；
- 每天 22:00–次日 08:00 只把待机动作换成睡觉，其他工作状态不变；
- 不创建“一二（睡觉）”或“布布（睡觉）”等独立角色。

安装完成后重启 ChatGPT/Codex，进入 `设置 → Pets`，选择“一二”或“布布”。如果睡眠时间切换后浮窗没有立即刷新，下次启动应用时一定会读取新的图集。

如果希望先查看脚本再执行：

```powershell
git clone --branch v1.1.0 https://github.com/skye-luo/yier-bubu-codex-pet.git
cd yier-bubu-codex-pet
powershell -ExecutionPolicy Bypass -File .\install.ps1
powershell -ExecutionPolicy Bypass -File .\install-sleep-mode.ps1
```

手动测试 Windows 睡眠切换：

```powershell
powershell -ExecutionPolicy Bypass -File "$HOME\.codex\yier-bubu-pet-sleep-mode\pet_sleep_scheduler.ps1" -Mode Sleep
powershell -ExecutionPolicy Bypass -File "$HOME\.codex\yier-bubu-pet-sleep-mode\pet_sleep_scheduler.ps1" -Mode Awake
```

Windows 卸载（文件会移动到备份目录，不会直接删除）：

```powershell
powershell -ExecutionPolicy Bypass -File .\uninstall-sleep-mode.ps1
powershell -ExecutionPolicy Bypass -File .\uninstall.ps1
```

### macOS

```bash
curl -fsSL https://raw.githubusercontent.com/skye-luo/yier-bubu-codex-pet/v1.1.0/quick-install.sh | bash
```

这条命令会安装两个宠物并启用 22:00–08:00 自动睡眠。安装完成后重启 Codex，进入 `设置 → 外观 → Pets`，选择“一二”或“布布”。

如果你希望先查看脚本再执行，也可以使用透明的分步安装：

```bash
git clone --branch v1.1.0 https://github.com/skye-luo/yier-bubu-codex-pet.git
cd yier-bubu-codex-pet
bash install.sh
bash install-sleep-mode.sh
```

`install-sleep-mode.sh` 会启用自动睡眠：

- 设置中始终只有“一二”和“布布”，不会注册独立睡觉角色；
- 每天 22:00 将待机行换成睡觉，08:00 恢复普通待机；
- 工作、等待确认、检查等其他状态不变；
- 每 5 分钟校正一次，并在登录或唤醒后立即按本地时间校正；
- Codex 已运行时会尝试立即刷新宠物浮窗，否则下次启动时生效。

手动测试：

```bash
python3 ~/.codex/yier-bubu-pet-sleep-mode/pet_sleep_scheduler.py --mode sleep
python3 ~/.codex/yier-bubu-pet-sleep-mode/pet_sleep_scheduler.py --mode awake
```

## 校验与卸载

```bash
bash verify.sh
bash uninstall-sleep-mode.sh
bash uninstall.sh
```

卸载脚本不会直接删除文件，而会移动到 `~/.codex/pets-backups/`，方便恢复。

## 项目结构

```text
.
├── pets/
│   ├── yier/
│   └── bubu/
├── sleep-source/
├── docs/
├── scripts/
├── launchd/
├── social/xiaohongshu/
├── install.ps1
├── install-sleep-mode.ps1
├── quick-install.ps1
├── uninstall.ps1
├── uninstall-sleep-mode.ps1
├── verify.ps1
├── install.sh
├── install-sleep-mode.sh
├── quick-install.sh
├── uninstall.sh
├── uninstall-sleep-mode.sh
└── verify.sh
```

安装脚本和项目说明采用 MIT 许可，见 [LICENSE-CODE.md](LICENSE-CODE.md)。角色名称、形象、动画图集及预览图片不在 MIT 许可范围内。
