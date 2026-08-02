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

## 一行安装（macOS）

```bash
curl -fsSL https://raw.githubusercontent.com/skye-luo/yier-bubu-codex-pet/v1.0.1/quick-install.sh | bash
```

这条命令会安装两个宠物并启用 22:00–08:00 自动睡眠。安装完成后重启 Codex，进入 `设置 → 外观 → Pets`，选择“一二”或“布布”。

如果你希望先查看脚本再执行，也可以使用透明的分步安装：

```bash
git clone --branch v1.0.1 https://github.com/skye-luo/yier-bubu-codex-pet.git
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
├── install.sh
├── install-sleep-mode.sh
├── quick-install.sh
├── uninstall.sh
├── uninstall-sleep-mode.sh
└── verify.sh
```

安装脚本和项目说明采用 MIT 许可，见 [LICENSE-CODE.md](LICENSE-CODE.md)。角色名称、形象、动画图集及预览图片不在 MIT 许可范围内。
