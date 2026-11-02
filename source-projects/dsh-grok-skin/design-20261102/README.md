# Grok娘 · 绯月邀约

2026-11-02 · v0.2.0 · 已实装至本机 DeepSeek Harness。

## 当前交付

- 皮肤本体：`skin/grok-crimsoncourt-dsh/`，v2 清单、完整明暗令牌、组件样式与原生界面适配。
- 新版美术：24 枚透明底绘制器物图标、黑金玫瑰牌匾、雕金丝绒输入框、侧栏材质。均由内置 imagegen 依据干净母图和视觉卡生成；没有用视频截图作角色参考。
- 当前动画：`source/grok-feiyue-bg-loop-v3.mp4`，用户交回的 Grok Bot v3；1920×1080、30fps、约16.03秒、无声。前约12秒为正向主片，后约4秒为回程桥接；未额外倒放或重新编码。
- 离线预览：`preview/index.html`，包含首页、会话、询问、审批、图标、账户菜单与设置。示例余额、模型、会话均为设计数据。
- 参考在 `references/`，完整生图提示词在 `prompts/`，五张绘制素材原件在 `source/raster-v1/`，构建代码在 `source/`。
- 当前实际使用 CSS、PNG/JPG 和 MP4；没有 hooks.mjs，没有修改 DSH 核心或共享插件。旧 SVG 与轻动态稿保留在工程历史中，当前样式不引用它们。

## 切换与本机实装

本机已安装五套皮肤：Gemini Starwork 0.1.7、Qianwen Moon Porcelain 0.3.1、ChatGPT Silver Court 0.4.2、DeepSeek Tidalglass 0.1.0、Grok Crimson Invitation 0.2.0。

切换入口：左下角头像/账号菜单 → 设置 → 皮肤 → 对应卡片的“应用”。可以先“试穿”。使用已有 Skin Center 热切换，选择会保存；当前为 Grok。没有另装重复的切换插件。

安装目录为 `/Users/qianweitao/.dsh/skins/grok-crimsoncourt-dsh/`。本轮安装和五套切换已在真实原生界面逐一确认，最后回到 Grok。选择状态已备份在本工程 `install-20261102/`，真实界面验收截图也在该目录；这些本机记录不放入公开源码包。

其他电脑可将本体 ZIP 解压为 `grok-crimsoncourt-dsh/skin.json`，把整个主题目录放入当地的 DSH 用户 skins 目录，再从皮肤中心应用。不要把整个源码工程放入 skins。

## 构建与预览

运行 `python3 -X utf8 source/build.py`，从 theme.json、绘制 PNG 和样式重建皮肤及预览。构建不会自动安装或切换。

父目录同时包含 dsh-grok-skin 和 dsh-deepseek-skin 时，在本工程运行 `python3 source/serve.py --port 8772`，访问：
`http://127.0.0.1:8772/dsh-grok-skin/design-20261102/preview/index.html`。

`preview/motion-player.html` 可查看实际 v3 视频，提供跳到桥接处与首尾接缝的按钮。旧 WebGL 轻动态工作稿与旧视频仅作为制作记录保留，当前成片以明确标记的 v3 为准。

## 参考盘点与设计取舍

- 原立绘：references/grok-user-original.png（Drive 1LG7wqyyOtK3_EnPm9FtLc-tgc8dbnbMI）。
- 派生三视图：references/grok-visual-card-v1.png（Drive 1wxCAmy8YqN88GHCg0J9aIzkRSt8budYW）。
- 表情母版：references/grok-face-master.png（Drive 19-nIJgEYliZLKw69PYlyFR-4bicoMMgi）。

三张均已逐张目检。三视图、表情母版为原工程派生参考，不当作新增官方原立绘；未声称取得全部历史版本。保留金发双马尾、蓝眼、精灵耳、月冠、黑金礼裙与酒红衬里，以及一把 X 型撑架战斧。场景、坐姿和新材质为主题改编。

v1 右侧坐姿大厅被认为构图雷同；v2 左侧扶栏姿势不自然；v3 站姿被认为平庸；v4 窗边近景获用户明确认可。0.2 依用户要求把图标、输入框、牌匾和侧栏提升为生成素材，参考千问/ChatGPT 既有组件的完成度；角色造型依旧以 Grok 自身参考为准。

五份生成提示词：icon-nav-atlas.txt、icon-controls-atlas.txt、composer-raster-v1.txt、brand-raster-v1.txt、sidebar-raster-v1.txt。均为内置 imagegen 的参考图编辑/派生模式。未调用额外付费图像 API，未在本机运行大模型。

## 验看范围

离线预览已检查整体、24 图标放大与实际尺寸、审批/询问底板、设置文字以及短窗口工作区。新版原生界面确认了导航、工作区、输入框、牌匾、HARNESS 字样对比和五套热切换。原生动态背景已经显示；未把解码通过等同于首尾运动完美，也未触发真实权限命令来测试审批。第三方插件内部没有稳定标记的图标仍可能由宿主绘制，不能据此宣布全部插件界面兼容。

新增检查脚本、探针、日志程序：无。build*.py 为构建代码，serve.py 为离线预览服务。

## 素材归属与打包

人物原设和参考由用户提供；主题图像为 AI 辅助派生，商标及第三方权利不因本工程转移。源码包包含参考、提示词、可构建源文件与设计预览，不包含账号配置、凭据、真实会话或本机安装截图。旧版本、备份及交付包继续保留。没有执行 GitHub 上传。
