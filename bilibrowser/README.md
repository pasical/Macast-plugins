# BiliBrowser

## English

BiliBrowser renderer for Macast. It opens the original Bilibili video in your default browser.

### Platform

darwin win32 linux

### Dependence

Requires [NVA (Nirvana) Protocol](https://github.com/xfangfang/Macast-plugins/blob/main/nirvana/README.md)  plugin to resolve aid/cid. **After installing, switch the adapter to NVA in Macast settings.**

### Help

Download the plugin to the renderer folder, enable BiliBrowser in Macast. When you cast a Bilibili stream to Macast, the plugin  opens ```https://www.bilibili.com/video/BV...```. Make sure to manually switch the adapter option to NVA; otherwise, your browser will open an m3u8 player.

## 中文

BiliBrowser 是为 Macast 开发的播放器插件，会在默认浏览器中打开哔哩哔哩视频源链接。

### 平台

darwin win32 linux

### 依赖

依赖 [NVA 协议](https://github.com/xfangfang/Macast-plugins/blob/main/nirvana/README.md) 用于解析 aid/cid。**安装后请在 Macast 的适配器设置中手动切换为 NVA。**

### 使用帮助

将插件放在 renderer 文件夹，在 Macast 中启用 "BiliBrowser"。当向 Macast 投送 B 站内容时，插件会在浏览器打开 ```https://www.bilibili.com/video/BV...```。请务必手动将适配器选项切换为 NVA，否则浏览器会直接打开 m3u8 播放器。