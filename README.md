# 安安的素描本聊天框的NoneBot插件

[![License](https://img.shields.io/github/license/ZiAzusa/nonebot_plugin_anans_sketchbook)](LICENSE)
[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/downloads/)
[![Nonebot](https://img.shields.io/badge/nonebot-v2.0.0-rc3)](https://nonebot.dev/)
[![Onebot](https://img.shields.io/badge/OneBot-v11-black?style=social&logo=data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAEAAAABABAMAAABYR2ztAAAAIVBMVEUAAAAAAAADAwMHBwceHh4UFBQNDQ0ZGRkoKCgvLy8iIiLWSdWYAAAAAXRSTlMAQObYZgAAAQVJREFUSMftlM0RgjAQhV+0ATYK6i1Xb+iMd0qgBEqgBEuwBOxU2QDKsjvojQPvkJ/ZL5sXkgWrFirK4MibYUdE3OR2nEpuKz1/q8CdNxNQgthZCXYVLjyoDQftaKuniHHWRnPh2GCUetR2/9HsMAXyUT4/3UHwtQT2AggSCGKeSAsFnxBIOuAggdh3AKTL7pDuCyABcMb0aQP7aM4AnAbc/wHwA5D2wDHTTe56gIIOUA/4YYV2e1sg713PXdZJAuncdZMAGkAukU9OAn40O849+0ornPwT93rphWF0mgAbauUrEOthlX8Zu7P5A6kZyKCJy75hhw1Mgr9RAUvX7A3csGqZegEdniCx30c3agAAAABJRU5ErkJggg==)](https://onebot.dev/)
[![Onebot](https://img.shields.io/badge/OneBot-v12-black?style=social&logo=data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAEAAAABABAMAAABYR2ztAAAAIVBMVEUAAAAAAAADAwMHBwceHh4UFBQNDQ0ZGRkoKCgvLy8iIiLWSdWYAAAAAXRSTlMAQObYZgAAAQVJREFUSMftlM0RgjAQhV+0ATYK6i1Xb+iMd0qgBEqgBEuwBOxU2QDKsjvojQPvkJ/ZL5sXkgWrFirK4MibYUdE3OR2nEpuKz1/q8CdNxNQgthZCXYVLjyoDQftaKuniHHWRnPh2GCUetR2/9HsMAXyUT4/3UHwtQT2AggSCGKeSAsFnxBIOuAggdh3AKTL7pDuCyABcMb0aQP7aM4AnAbc/wHwA5D2wDHTTe56gIIOUA/4YYV2e1sg713PXdZJAuncdZMAGkAukU9OAn40O849+0ornPwT93rphWF0mgAbauUrEOthlX8Zu7P5A6kZyKCJy75hhw1Mgr9RAUvX7A3csGqZegEdniCx30c3agAAAABJRU5ErkJggg==)](https://onebot.dev/)

本分支是 [MarkCup-Official/Anan-s-Sketchbook-Chat-Box](https://github.com/MarkCup-Official/Anan-s-Sketchbook-Chat-Box) 的Nonebot插件。

## 部署

将本项目clone到Nonebot的插件目录并安装依赖：

```
cd 插件目录
git clone https://github.com/ZiAzusa/nonebot_plugin_anans_sketchbook.git
cd nonebot_plugin_anans_sketchbook
pip install -r requirements.txt
```

或者，将本项目所在路径直接引入到Nonebot的bot.py

如需添加表情/修改字体，可以直接修改config.yaml

## 配置参数

主要可配置项包括：
- 文本框和图片框的坐标范围
- 字体文件路径
- 底图和遮罩图路径

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

<img src="sources/example.jpg?raw=true" alt="使用例" style="width: 50%;">

## 许可证

本项目基于MIT协议传播，仅供个人学习交流使用，不拥有相关素材的版权。进行分发时应注意不违反素材版权与官方二次创造协定。

<hr>

更多信息请查看原项目 [MarkCup-Official/Anan-s-Sketchbook-Chat-Box](https://github.com/MarkCup-Official/Anan-s-Sketchbook-Chat-Box)
