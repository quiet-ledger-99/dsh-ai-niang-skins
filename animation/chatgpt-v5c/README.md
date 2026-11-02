# 收到的 v5c 动画资料

当前采用 **v5c**，不要按文件名大小自动改成未采用的 v6/v7。皮肤成品在 `../../skins/chatgpt-silvercourt-dsh/`。

- `received-source/`：收到的 `blink.py`、`common.py`、`build_v5c.py`，保留其原始内容，本次未执行。
- `inputs-and-notes/`：v5b 输入视频及 v5b/v5c 交付说明。
- `qa/`：提供方的眨眼序列和脸部对比图。

## 可复现边界

`common.py` 引用原作者环境 `/workspace/chatgpt-skin-bg/v5b_work/` 下的：

- `ts_1.5_3.0.json`
- `src/*.png`
- `sr/*.png`

这些上游时间映射和中间帧不在本机收到的资料中，现有脚本不能独立重渲染出原 v5c。依赖还包括 Python、NumPy、OpenCV 和 FFmpeg。

保留 v5b MP4 不等于补齐上述中间帧。GrokBot 如果仍持有原工程，可后续补源；本次上传任务不需要重做或替换用户已经确认的 v5c。
