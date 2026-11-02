# DeepSeek Harness · 五套AI拟人娘主题皮肤

当前交付快照：2026-11-02。五套皮肤可并存，通过DSH现有皮肤中心切换。

| 主题 | 版本 | 当前背景 |
|---|---|---|
| Gemini娘 · 星光工作台 | 0.1.7 | 星夜PNG＋图片/CSS动效 |
| 千问娘 · 月下青瓷 | 0.3.1 | 16秒月夜轻动态 |
| ChatGPT娘 · 云上银庭 | 0.4.2，含当前手机工作区补丁 | 用户确认的v5c |
| DeepSeek娘 · 澄潮绮窗 | 0.2.0 | 坐姿母图v3对应的视频v4 |
| Grok娘 · 绯月邀约 | 0.2.0 | 绯月窗边母图v4对应的视频v3 |

完整工作内容、验收范围、媒体规格与缺项，见[五套皮肤工作报告](docs/五套皮肤工作报告-20261102.md)。许可按[原始声明](LICENSE-NOTICE.md)保留，不额外授予统一开源许可。

## 安装与切换

每套都是skinManifestVersion: 2的独立静态资产目录。将所选skins/<id>/整个复制到自己的DSH用户skins目录，再从左下角头像 → 设置 → 皮肤 → 试穿/应用。选择由皮肤中心保存。

不需要复制账号、profile或制作环境。运行只使用清单声明的CSS/图片/视频，制作JS/Python留在工程侧。已有实装记录不等于全部核心版本、插件页或移动端场景均兼容。

## 目录

- skins/：当前发布/安装入口。
- source-projects/：源码、母图、提示词与设计预览，内含对齐的当前skin镜像；早期设计页按历史保留。
- docs/history/：过程与交付记录。
- docs/current-overrides/：ChatGPT同版当前手机补丁的差异说明。
- animation/chatgpt-v5c/：收到的动画加工资料与缺项。

ChatGPT的样式入口为skin-inkwhite.css和patches-inkwhite.css，不要统一改写成skin.css。DeepSeek/Grok可在各工程目录运行python3 -X utf8 source/build.py重建；背景视频作为已交付输入保留。上游生视频中间数据的缺项不影响现有本体运行，具体见工作报告。

## 查看设计预览

在仓库根目录运行python3 -m http.server 8771 --bind 127.0.0.1，然后打开：

- Gemini：/source-projects/dsh-gemini-skin/design-20261028/index.html
- 千问：/source-projects/dsh-qianwen-skin/design-20261029/preview/index.html
- ChatGPT：/source-projects/dsh-chatgpt-skin/design-20261029/preview/index.html
- DeepSeek：/source-projects/dsh-deepseek-skin/design-20261102/preview/index.html
- Grok：/source-projects/dsh-grok-skin/design-20261102/preview/index.html

这些是制作/设计预览，示例余额、模型或审批内容不代表真实运行事件。原生账号/会话截图、完整历史、运行日志和本机备份不入库。

## 随包预览图

Gemini：审批样式预览。
![Gemini](skins/gemini-starwork-dsh/preview/light.jpg)

千问：月下青瓷。
![千问](skins/qianwen-moonporcelain-dsh/preview/light.jpg)

ChatGPT：珍珠白与黑边纹。
![ChatGPT](skins/chatgpt-silvercourt-dsh/preview/court-v0.4.png)

DeepSeek：海馆藏珍v0.2。
![DeepSeek](skins/deepseek-tidalglass-dsh/preview/cover.jpg)

Grok：黑金绯月v0.2。
![Grok](skins/grok-crimsoncourt-dsh/preview/cover.jpg)
