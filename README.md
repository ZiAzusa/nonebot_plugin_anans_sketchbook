# 安安的素描本聊天框的NoneBot插件

本分支是 [MarkCup-Official/Anan-s-Sketchbook-Chat-Box](https://github.com/MarkCup-Official/Anan-s-Sketchbook-Chat-Box) 的Nonebot插件。

## AI声明

本项目90%的代码由AI生成

## 部署

将本项目clone到Nonebot的插件目录并安装依赖：

```
cd 插件目录
git clone https://github.com/ZiAzusa/nonebot_plugin_anans_sketchbook.git
cd nonebot_plugin_anans_sketchbook
pip install -r requirements.txt
```

或者，将本项目所在路径直接引入到Nonebot的bot.py

## 使用

```
命令：anan 或 夏目安安
功能：生成夏目安安的素描本聊天框
支持的差分表情：{', '.join(config.baseimage_mapping.keys())}

用法：夏目安安 ?可选差分 文本/图片（优先图片）

例如：夏目安安 开心 这是吾辈在【说话】

示例：
夏目安安 这是吾辈在说话
夏目安安 开心 吾辈开心
夏目安安 [图片]
夏目安安 开心 [图片]
```

<hr>

**以下是原项目README**

## AI声明

本项目90%的代码由AI生成

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

