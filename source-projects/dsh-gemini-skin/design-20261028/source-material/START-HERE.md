# Gemini 娘主题 0.2.1 → DeepSeek Harness 研究交接

交给已有任务「研究 DeepSeek Harness 皮肤适配」；任务 ID 01a1829a-66ba-7112-9468-da838f42bdbb，本机工作目录 /Users/qianweitao/Projects。此包用于该任务已有适配研究，不授权新宿主安装或扩大访问权限。

先看 ART/runtime（当前 36 张），ART/reference（身份卡、指定星形、认可组件配色板）和 EXTENSION。ART/extras 汇总去重的原始图集、补充图标和历史变体；其中有被后续轻盈纸艺方向取代的机械底板初稿，不要误当最新方案。

## 角色与设计方向

蓝紫长发渐淡紫粉，双发髻、猫耳猫尾、呆毛；正视画面左粉红眼/右金眼；角色自身左侧（画面右）金边紫蓝星饰。以角色卡实际图像为准。四芒星必须是用户指定的上下长尖、左右短尖、金边紫蓝切面星，不能改成 Unicode 星号。蓝紫/深靛/冷白为基底，允许彩虹光谱、金边与红粉点色。保持已认可像素构形、纸艺底板和阅读区，不靠大角色贴图代替组件设计。

## 真实状态：不要把测试数写成实机成功

- 原 33 项回归：实际固定上游 renderer/CSS + 隔离 WKWebView，输入/选择/聊天切换/尺寸/清理/眨眼尾摆/暂停等通过。见 REPORTS/integration-lifecycle.json。
- 11 项失败类型复现：非语义侧栏、强样式冲突、窄图标栏和不活动页面等合成条件通过。不是从真实宿主采集的完整 DOM，见 failure-replay-result.json。
- 11 项安装器模拟：临时假引擎 + 桩调用，幂等、回滚、摘要拒绝通过；没有执行真实上游安装/启动/恢复脚本，见 installer-fixture-tests.json。
- 旧 0.2.0 由用户实际安装时失败。交付文件 SHA256、版本、ID、revision 一致，但 geminiSurfacePass/visualReady 为 false，identity/navigation 为 0；截图出现白字浅底、标题导航缺失、输入底板不全。旧日志不能单独证明是哪一处底板导致最终 false。
- 0.2.1 已在本地修正独立输入底层、样式租约、侧栏结构回退、窄栏/非活动页过滤和逐部件诊断；真实 ChatGPT **尚未通过复验**。文件回滚曾确认恢复到原引擎；未探测当前真实应用/CDP 状态。

## 不可直接平移到 DeepSeek 的部分

THEME 是第三方 Dream Skin 1.9.0 的受限主题格式；EXTENSION 的 app: 限定、ChatGPT/Codex 选择器、生命周期全局变量、补丁、引擎目录和注入机制均为该宿主专用，不是 DeepSeek 插件协议。

适配研究可直接复用位图/帧表/颜色与组件构形；应先查 DeepSeek Harness 自己的受支持皮肤接口，再重写宿主绑定、布局和状态源。不要运行此包中的 ChatGPT 安装器/注入器来试探 DeepSeek。CHATGPT-INSTALLER-REFERENCE 和 UPSTREAM-REFERENCE 仅供审阅；.command 在归档内不设执行位，原 Mac 路径不可移植。

固定代理门禁 BLOCKED_AGENT_HOST_ACCESS / com.openai.codex 访问拒绝继续保留；本交接不是绕过许可。没有新的自动启动、CDP 连接或凭据。

## 未完成及真实限制

环境流星/星轨等没有全部进入当前扩展；眨眼/尾摆在首页工作，聊天按原设计暂停。真实模型/额度/任务完成 API 未接入，不把未知额度画成 0，不把演示数值当真实数据。全部菜单、设置子页、代码编辑器及所有宿主路由未覆盖验收。Q 版/全身素材已提供，但不能冒充所有状态都已与真实事件绑定。

## 完整性与使用

EXTENSION/gemini-v11-payload.js 的 SHA256 为 `1eff6702d00ad4c57680dcb8206fc1e4348338a7e57b1f94c489ff8552e14ab5`。这是包含素材的旧宿主载荷，不应直接在 DeepSeek 执行。

若只验证素材与源码对应，在解压根目录运行 `node BUILD/verify-rebuild.mjs`（Node 20+）。它只读文件并生成字符串比较，不执行 renderer/installer，不访问宿主。原 QA 脚本保留原工程相对布局，位于 QA/original-project-scripts，不能把它们当解压后的一键测试入口。

CONTENT-MANIFEST.json 列逐文件长度/SHA256，SHA256SUMS.txt 包含清单自身摘要，二者不自哈希。没有原始安装日志、真实用户截图、config.toml、config-before、凭据或其他会话；只有去内容的错误字段与合成测试记录。

软件参考上游 MIT 许可已保留；用户提供的角色参考与生成美术仅沿用现有私有评估范围，没有声明第三方人物素材版权自动转移。未复制原超天酱人物素材，未重新生图。
