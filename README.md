# 一二 × 布布：项目已合并

新版统一入口：**[一二 × 布布 × 点仔 Codex Pets](https://github.com/skye-luo/yier-bubu-codex-pets)**（仓库名称末尾是复数 `pets`）。

本仓库的一二、布布、Windows 安装和自动睡眠功能已并入主项目。新版更新了形象、查资料 / 写代码 / 写作的持续工作造型，以及 16 个注视方向；点仔也在主项目中继续保留。

## 安装或更新

直接告诉 Codex：

> 帮我安装或更新 https://github.com/skye-luo/yier-bubu-codex-pets 里的宠物。

Windows 打开 PowerShell：

```powershell
irm https://raw.githubusercontent.com/skye-luo/yier-bubu-codex-pets/v2.0.0/quick-install.ps1 | iex
```

macOS 打开终端：

```bash
curl -fsSL https://raw.githubusercontent.com/skye-luo/yier-bubu-codex-pets/v2.0.0/quick-install.sh | bash
```

装好后重启 Codex，在「设置 → Pets」选择角色。安装器会备份原宠物、合并旧定时组件；夜间 22:00–08:00 无任务时睡觉，不额外添加睡觉版角色。

## 兼容和历史

- 本仓库保留，不删除历史提交、标签或 Release，旧版本下载链接继续可用。
- 本仓库 `main` 上的两个 `quick-install` 脚本转向统一项目。
- 其他旧文件仅作为历史兼容保留；后续更新、问题反馈和分享请使用统一入口。
- [原版本说明](README-legacy.md) · [历史版本](https://github.com/skye-luo/yier-bubu-codex-pet/releases)

非官方、非商业粉丝体验版。代码许可与角色素材权利声明继续适用，详见 [ASSET-NOTICE.md](ASSET-NOTICE.md)。
