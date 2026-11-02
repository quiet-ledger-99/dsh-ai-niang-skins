# DeepSeek娘 · 澄潮绮窗

2026-11-02 · v0.2.0 · 已实装至本机 DeepSeek Harness。

## 当前设计

以角色的蓝白女仆服、鲸尾、珍珠与海底书房为依据，将主题做成一套完整的海馆藏珍器物界面。靛蓝提供安静底色，白贝与蓝白珐琅承担装饰，银色细轨和少量黄铜连接材质。装饰集中于外围和转角，文字、消息内容及工作区保持清楚。

本轮不是另换背景图：保留用户选定的坐姿修订母图v3和 Grok Bot 动画v4，把此前较早的图标、输入框、牌匾、侧栏和决策面板补齐到同组主题的设计完成度。后续修订应主动检查整套组件，不以“背景已接入、能显示”作为设计完成标准。

## 实际使用的素材

六张素材均由内置 imagegen 生成，完整原件在 source/raster-v1/，完整提示词在 prompts/ 同名txt：

| 素材 | 用途 |
|---|---|
| icon-nav-atlas.png | 12枚导航器物：插件、潮汐钟、任务图册、记忆书、更多、搜索、筛选、工作区、文件夹、手机、远程通讯 |
| icon-controls-atlas.png | 12枚控件器物：设置、反馈、登出/登录、附件、权限、发送、模型、预设、鲸徽、新会话、关闭 |
| composer-raster-v1.png | 鲸尾、贝壳、蓝缎带与珍珠组成的输入框边饰，中央透明 |
| brand-raster-v1.png | 真实 DeepSeek/HARNESS 字样下方的深蓝珐琅牌匾 |
| sidebar-raster-v1.png | 低对比靛蓝藏书封面材质；明亮装饰限制在边缘 |
| panel-frame-raster-v1.png | 审批、询问、设置及菜单共用的贝壳珍珠边框 |

两张图集均为1448×1086 RGBA，4列×3行；两个横框2172×724 RGBA；面板框1254×1254 RGBA；侧栏821×1916 RGB。通过图集定位和可伸缩边框接入原生控件。没有用视频截图当人物参考，也没有用SVG替代这六张新素材。旧SVG文件保留在工程历史中，当前生成的样式不引用它们。

## 动态背景

当前视频：source/deepseek-chengchao-bg-loop-v4.mp4；1920×1080、30fps、427帧、约14.23秒、无声H.264。静态海报为 source/wallpaper-v3-seated.png。视频由用户交回，本轮没有重压、倒放、增加滤镜或交叉淡化。

视频交接方说明：约11.27秒主片＋约2.97秒正向回程桥接；桥接纹理与主片可能略有差别，尾鳍快摆处可能有轻微插帧拖影。保留 source/成片交付说明-v4.md 和 source/给ChatGPT-嵌皮肤交接-v4.md，不把接入成功宣传成运动接缝完美。

## 原生适配与实装

安装目录：/Users/qianweitao/.dsh/skins/deepseek-tidalglass-dsh/。
切换入口：左下角头像 → 设置 → 皮肤 → 对应主题“应用”。同一皮肤ID继续使用，其他四套和公共播放器未改。

- 原生侧栏导航、Tripo Studio入口、工作区工具、底部入口、附件、发送、新会话等配上了新图集；实际设置窗口保留可读的浅色卡片，关闭按钮使用配套图标。
- 输入框九宫格边饰控制在边缘，保留文字与工具栏空间；上方工作区/模式按钮有浅色底衬，避免压在深色裙面上难读。
- 已完成的旧会话未必保留 streaming-body 标记，因此用已有 chat-flow 标记补上磨砂阅读底板，修复正文直接叠在插画上的问题。
- 沿用v0.1.1已修复的40px媒体起点，顶端没有重复的静态海报条；欢迎标题在右上，避开额头。
- 菜单和设置的装饰不改变宿主浮层定位；图集不改变按钮动作、权限或发送逻辑。

原生验收：空首页、真实旧会话阅读、全局导航、工作区空间和账户设置卡片已实际查看；账户菜单功能入口已使用，菜单图标及询问/审批完整外观另有离线预览截图。未触发真实权限命令，也没有声称所有第三方插件内部图标和页面均已定制。

真实账号、余额及会话截图仅在 install-raster-20261102/，不纳入公开交付。screenshots/ 内带 raster-020 的图是离线设计预览，示例余额/会话不连接真实模型。

## 构建与预览

在本工程目录运行：python3 -X utf8 source/build.py。
构建依次打包PNG、生成颜色与组件样式、绑定图集及边框，并重建预览；不会自动安装或切换。

预览服务：python3 source/serve.py --port 8772。
父目录保留 dsh-deepseek-skin/design-20261102/ 结构后访问：
http://127.0.0.1:8772/dsh-deepseek-skin/design-20261102/preview/index.html

preview/motion-player.html 可单独播放当前v4。source/motion-source.html、motion.js、旧眨眼帧及旧视频为早期制作记录，不是当前运行输入。

## 参考盘点

已逐张查看可取得的三份角色原工程参考，并回看当前静态母图：
- references/deepseek-user-original.png：用户原立绘，Drive 1f_b6iExBAnB1B2dFLHZA_rzfJZrq9ZIr。
- references/deepseek-visual-card-v2.png：鲸尾修订视觉卡，Drive 1S9Q-uFPgOag_QxhkC79BTQXUULSytc8_。
- references/deepseek-face-master.png：表情母版，Drive 1zGkwnhw5KScMj7qPELLOaVYBFnslpCDk。

视觉卡和表情母版是原工程派生参考，不冒充新增官方原立绘；未声称获得全部历史版本。UI质量参考位于 references/ui-quality/，来自用户既有千问和ChatGPT输入框，只借鉴完成度与组件留白，不替代DeepSeek角色依据。海底书房、场景器物和新UI装饰是本主题改编。

## 版本与备份

v0.1.0：桌前海窗母图v2及早期SVG界面/轻动态示意。
v0.1.1：接入坐姿v3对应的动画v4，修正顶部静态重复条、标题位置和HARNESS对比。
v0.2.0：六张新绘制素材、24图标、整套组件边框及真实旧会话阅读底板；保留v4视频。

本轮备份：backups/before-raster-20261102-144300/，含原源码入口和改前项目/正式皮肤；此前v4备份、旧视频和交付ZIP全部保留。没有改DSH核心、插件版本、profile或其他主题，没有上传GitHub。

新增检查脚本、探针、监控或日志程序：无。build-assets-raster.py和build-raster.py是素材构建/绑定代码；图集JSON是实际资源配置，motion-player.html是用户播放预览。

人物、商标及第三方素材权利不因本工程转移。公开源码包包含可重建源文件、提示词、参考和设计预览，不含账号配置、凭据、真实会话、原生验收截图或备份。
