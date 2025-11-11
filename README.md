# 安安的素描本聊天框的NoneBot插件

**未完成，暂不可用**

本分支是 MarkCup-Official/Anan-s-Sketchbook-Chat-Box 的Nonebot插件。

## AI声明

本项目90%的代码由AI生成

## 使用示例

- 文本生成：向机器人发送消息或命令 `/anan 你好`，机器人会返回生成的图片。
- 图片粘贴：直接发送图片，机器人会将该图片粘贴到底图指定的位置并返回结果。

安装依赖后，将本仓库所在路径加入 Python 路径（或将插件包安装到 environment），并在 nonebot 配置中加载 `nonebot-plugin-anan-s-sketchbook`。

安装依赖：
```bash
pip install -r requirements.txt
```

<hr>

**以下是原项目README**

## 部署

本项目只支持 windows ，如果你使用 macos 或者 linux 请参考 [这个分支](https://github.com/Sheyiyuan/Anan-s-Sketchbook-Chat-Box)

现在字体文件和安安图片已经内置于项目中, 无需再额外置入DLC.

其中`font.ttf`为字体文件, 可以自由修改成其他字体, 本项目不拥有字体版权, 仅做引用.

底图存储于`BaseImages`目录中, 其中`base.png`为安安拿素描本的照片, `base_overlay.png`为透明底的安安袖子, 用于防止文字和图片覆盖在袖子上方. 如果分辨率不一样的安安图片, 需要修改`config.py`的 `TEXT_BOX_TOPLEFT` 和 `IMAGE_BOX_BOTTOMRIGHT`, 定义文本框的大小.

依赖库安装: `pip install -r requirements.txt `

## 使用

使用文本编辑器打开`config.py`即可看到方便修改的参数, 可以设置热键, 图片路径, 字体路径, 指定的应用, 表情差分关键词等

运行`main.py`即可开始监听回车, 在指定应用中按下回车会自动拦截按键, 生成图片后自动发送 (自动发送功能可以在`config.py`中关闭).

特殊的, 在文本中输入\[\]或者【】, 被包裹的字符会变成紫色.

输入文本框中的图片也可以被直接绘制在素描本上.

输入`#普通#`, `#开心#`, `#生气#`, `#无语#`, `#脸红#`, `#病娇#`可以切换标签差分, 一次切换一直有效. 可以通过修改`BASEIMAGE_MAPPING`来增加更多查分

如果发送失败等可以尝试适当增大`main.py`第10行的`DELAY`

