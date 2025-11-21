<div align="center">

  <a href="https://nonebot.dev/"><img src="https://nonebot.dev/logo.png" width="200" height="200" alt="nonebot"></a>

# 安安的素描本聊天框的NoneBot插件

<p align="center">

[![License](https://img.shields.io/github/license/ZiAzusa/nonebot_plugin_anans_sketchbook)](LICENSE)
[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/downloads/)
[![Nonebot](https://img.shields.io/badge/nonebot-v2.0.0-rc3)](https://nonebot.dev/)
[![Onebot](https://img.shields.io/badge/OneBot-v11-black?style=social&logo=data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAEAAAABABAMAAABYR2ztAAAAIVBMVEUAAAAAAAADAwMHBwceHh4UFBQNDQ0ZGRkoKCgvLy8iIiLWSdWYAAAAAXRSTlMAQObYZgAAAQVJREFUSMftlM0RgjAQhV+0ATYK6i1Xb+iMd0qgBEqgBEuwBOxU2QDKsjvojQPvkJ/ZL5sXkgWrFirK4MibYUdE3OR2nEpuKz1/q8CdNxNQgthZCXYVLjyoDQftaKuniHHWRnPh2GCUetR2/9HsMAXyUT4/3UHwtQT2AggSCGKeSAsFnxBIOuAggdh3AKTL7pDuCyABcMb0aQP7aM4AnAbc/wHwA5D2wDHTTe56gIIOUA/4YYV2e1sg713PXdZJAuncdZMAGkAukU9OAn40O849+0ornPwT93rphWF0mgAbauUrEOthlX8Zu7P5A6kZyKCJy75hhw1Mgr9RAUvX7A3csGqZegEdniCx30c3agAAAABJRU5ErkJggg==)](https://onebot.dev/)
[![Onebot](https://img.shields.io/badge/OneBot-v12-black?style=social&logo=data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAEAAAABABAMAAABYR2ztAAAAIVBMVEUAAAAAAAADAwMHBwceHh4UFBQNDQ0ZGRkoKCgvLy8iIiLWSdWYAAAAAXRSTlMAQObYZgAAAQVJREFUSMftlM0RgjAQhV+0ATYK6i1Xb+iMd0qgBEqgBEuwBOxU2QDKsjvojQPvkJ/ZL5sXkgWrFirK4MibYUdE3OR2nEpuKz1/q8CdNxNQgthZCXYVLjyoDQftaKuniHHWRnPh2GCUetR2/9HsMAXyUT4/3UHwtQT2AggSCGKeSAsFnxBIOuAggdh3AKTL7pDuCyABcMb0aQP7aM4AnAbc/wHwA5D2wDHTTe56gIIOUA/4YYV2e1sg713PXdZJAuncdZMAGkAukU9OAn40O849+0ornPwT93rphWF0mgAbauUrEOthlX8Zu7P5A6kZyKCJy75hhw1Mgr9RAUvX7A3csGqZegEdniCx30c3agAAAABJRU5ErkJggg==)](https://onebot.dev/)

</p>

</div>

本分支是 [MarkCup-Official/Anan-s-Sketchbook-Chat-Box](https://github.com/MarkCup-Official/Anan-s-Sketchbook-Chat-Box) 的Nonebot插件，支持绘制文本/图片到安安的素描本上，也支持将Bot的所有文本消息替换为使用安安的素描本发送

## 部署

### 方案1 使用nb-cli或pip安装

nb-cli:
```shell
nb plugin install nonebot-plugin-anans-sketchbook
```
（未发布，请先使用pip）

pip:
```shell
pip install nonebot-plugin-anans-sketchbook
```

而后按照 [NoneBot加载插件](https://nonebot.dev/docs/tutorial/create-plugin#%E5%8A%A0%E8%BD%BD%E6%8F%92%E4%BB%B6) 加载插件

### 方案2 直接引入

将本项目clone到Nonebot的插件目录并安装依赖：
```shell
cd 插件目录
git clone https://github.com/ZiAzusa/nonebot_plugin_anans_sketchbook.git
cd nonebot_plugin_anans_sketchbook
mv nonebot_plugin_anans_sketchbook/* . && rm -rf nonebot_plugin_anans_sketchbook
pip install -r requirements.txt
```

## 配置

主要可配置项包括：
- 文本框和图片框的坐标范围
- 字体文件路径
- 底图和遮罩图路径
- 是否将Bot的所有文本消息替换为安安的素描本

如果通过nb-cli或pip安装，可以使用Nonebot的全局配置文件`.env.*`进行配置（也可以不进行配置，插件内置了默认配置文件），具体参考 [NoneBot配置](https://nonebot.dev/docs/appendices/config)

### 具体配置项如下

#### `ANAN__FONT_FILE`

- 类型：`str`
- 默认：`"resources/allseto.ttf"`
- 说明：使用字体的文件路径

#### `ANAN__TEXT_WRAP_ALGORITHM`

- 类型：`str`
- 默认：`"original"`
- 说明：文本换行算法，可选值："original"(原始算法), "knuth_plass"(改进的Knuth-Plass算法)

#### `ANAN__BASEIMAGE_MAPPING`

- 类型：`Dict[str, str]`
- 默认：
  ```python
  {
    "普通": "resources/BaseImages/base.png",
    "开心": "resources/BaseImages/开心.png",
    "生气": "resources/BaseImages/生气.png",
    "无语": "resources/BaseImages/无语.png",
    "脸红": "resources/BaseImages/脸红.png",
    "病娇": "resources/BaseImages/病娇.png",
    "闭眼": "resources/BaseImages/闭眼.png",
    "难受": "resources/BaseImages/难受.png",
    "害怕": "resources/BaseImages/害怕.png",
    "激动": "resources/BaseImages/激动.png",
    "惊讶": "resources/BaseImages/惊讶.png",
    "哭泣": "resources/BaseImages/哭泣.png"
  }
  ```
- 说明：将差分表情导入，默认底图base.png

#### `ANAN__BASEIMAGE_FILE`

- 类型：`str`
- 默认：`"resources/BaseImages/base.png"`
- 说明：默认底图文件路径

#### `ANAN__TEXT_BOX_TOPLEFT`

- 类型：`List[int]`
- 默认：`[119, 450]`
- 说明：文本框左上角坐标 (x, y), 同时适用于图片框

#### `ANAN__IMAGE_BOX_BOTTOMRIGHT`

- 类型：`List[int]`
- 默认：`[398, 625]`
- 说明：文本框右下角坐标 (x, y), 同时适用于图片框

#### `ANAN__BASE_OVERLAY_FILE`

- 类型：`str`
- 默认：`"resources/BaseImages/base_overlay.png"`
- 说明：置顶图层的文件路径

#### `ANAN__USE_BASE_OVERLAY`

- 类型：`bool`
- 默认：`True`
- 说明：是否启用底图的置顶图层, 用于表现遮挡

#### `ANAN__CONVERT_ALL_TO_ANAN`

- 类型：`bool`
- 默认：`False`
- 说明：是否将Bot的所有文本消息替换为安安的素描本（WARN：这是一个可能存在诸多Bug的实验性功能，开启该功能有损坏消息发送逻辑的风险，请谨慎启用）

#### `ANAN__MAX_LEN_OF_LONG_TEXT`

- 类型：`int`
- 默认：`150`
- 说明：如果Bot的消息的长度大于这个值，原样发送消息（避免因字体过小无法看清）

此外，如果通过直接引入的方式使用插件，可以直接修改config.yaml。

## 使用

```
命令：anan 或 夏目安安
功能：生成夏目安安的素描本聊天框

用法：夏目安安 ?差分 ?文本 ?图片

例如：夏目安安 开心 这是吾辈在【说话】

示例：
夏目安安 这是吾辈在说话
夏目安安 开心 吾辈开心
夏目安安 [图片]
夏目安安 开心 [图片]
夏目安安 开心 吾辈喜欢这个 [图片]
```

<img src="nonebot_plugin_anans_sketchbook/resources/example.jpg?raw=true" alt="使用例" style="width: 50%;">

## 许可证

本项目基于MIT协议传播，仅供个人学习交流使用，不拥有相关素材的版权。进行分发时应注意不违反素材版权与官方二次创造协定。

<hr>

更多信息请查看原项目 [MarkCup-Official/Anan-s-Sketchbook-Chat-Box](https://github.com/MarkCup-Official/Anan-s-Sketchbook-Chat-Box)
