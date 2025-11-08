# 安安的素描本聊天框

本项目是一个将你在一个文本输入框中的文字或图片写到安安的素描本上的项目

## AI声明

本项目90%的代码由AI生成

## 部署

本项目只支持windows

本项目不提供字体文件和安安图片, 需要你自己想办法加进来, 分别命名为`font.ttf`, `base.png`和`base_overlay.png`.
其中`font.ttf`为字体文件, `base.png`为安安拿素描本的照片, `base_overlay.png`为透明底的安安袖子, 用于防止文字和图片覆盖在袖子上方.
如果分辨率不一样的安安图片, 需要修改`config.py`的 `TEXT_BOX_TOPLEFT` 和 `IMAGE_BOX_BOTTOMRIGHT`, 定义文本框的大小.

依赖库安装: `pip install -r requirements.txt `

## 使用

使用文本编辑器打开`config.py`即可看到方便修改的参数, 可以设置热键, 图片路径, 字体路径等

运行`main.py`即可开始监听回车, 按下回车会自动拦截按键, 生成图片后自动发送 (自动发送功能可以在`config.py`中关闭).

如果发送失败等可以尝试适当增大`main.py`第10行的`DELAY`

详细教程: https://www.bilibili.com/opus/1131995010930049048

## 另外的分支
[增加了表情差分功能的分支, 暂不支持图片的插入](https://github.com/WrightHua/Anan-s-Sketchbook-Chat-Box/tree/main)