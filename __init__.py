from __future__ import annotations

import io
import base64
import logging
from typing import Optional, List, Tuple
from pathlib import Path

from PIL import Image
import httpx

from nonebot import on_command
from nonebot.adapters.onebot.v11 import Bot, Event, MessageSegment, Message
from nonebot.params import CommandArg

from .utils.image_fit_paste import paste_image_auto
from .utils.text_fit_draw import draw_text_auto
from .utils.config_loader import Config

config = Config.load()
logger = logging.getLogger(__name__)
logger.setLevel(config.logging_level)

usage = f"""\
命令：anan 或 夏目安安
功能：生成夏目安安的素描本聊天框
支持的差分表情：{', '.join(config.baseimage_mapping.keys())}

用法：夏目安安 ?可选差分 ?可选文本 ?可选图片

例如：夏目安安 开心 这是吾辈在【说话】
"""

# 命令触发器
anan = on_command("anan", aliases={"夏目安安"}, priority=5)

# 切到插件目录
def fix_path(filename: str) -> str:
    return str(Path(__file__).parent / filename)

# 根据参数列表获取处理后的参数列表和底图路径
def get_diff_info(args: List[str], has_image: bool) -> Tuple[List[str], str]:
    # 无参数，使用默认底图
    if not args:
        default_image = config.baseimage_mapping.get(None, config.baseimage_file)
        return args, fix_path(default_image)
    # 只有一个参数
    if len(args) == 1:
        # 如果没有图片，不判断差分
        if not has_image:
            default_image = config.baseimage_mapping.get(None, config.baseimage_file)
            return args, fix_path(default_image)
        # 如果有图片，判断差分
        else:
            if args[0] in config.baseimage_mapping.keys():
                diff_image = config.baseimage_mapping[args[0]]
                return [], fix_path(diff_image)
            else:
                default_image = config.baseimage_mapping.get(None, config.baseimage_file)
                return args, fix_path(default_image)
    # 两个以上参数，判断差分
    if args[0] in config.baseimage_mapping.keys():
        diff_image = config.baseimage_mapping[args[0]]
        return args[1:], fix_path(diff_image)
    # 其他情况
    default_image = config.baseimage_mapping.get(None, config.baseimage_file)
    return args, fix_path(default_image)

# 处理存在图片的情况
async def handle_image_content(img_url: str, base_image_path: str, text: str = "") -> bytes:
    # 下载图片
    async with httpx.AsyncClient() as client:
        resp = await client.get(img_url, timeout=20.0)
        resp.raise_for_status()
    img_bytes = resp.content
    # 1. 无文本
    if not text.strip():
        with Image.open(io.BytesIO(img_bytes)).convert("RGBA") as pil_img:
            return paste_image_auto(
                image_source=base_image_path,
                top_left=config.text_box_topleft,
                bottom_right=config.image_box_bottomright,
                content_image=pil_img,
                align="center",
                valign="middle",
                padding=12,
                allow_upscale=True,
                keep_alpha=True,
                image_overlay=fix_path(config.base_overlay_file) if config.use_base_overlay else None,
            )
    # 2. 有文本
    with Image.open(io.BytesIO(img_bytes)).convert("RGBA") as pil_img:
        x1, y1 = config.text_box_topleft
        x2, y2 = config.image_box_bottomright
        region_width = x2 - x1
        region_height = y2 - y1
        spacing = 10
        # 判断图片方向
        region_ratio = region_width / region_height
        is_vertical = pil_img.height * region_ratio > pil_img.width
        # 动态计算排版
        (img_tl, img_br, text_tl, text_br, text_font_height) = (
            # 竖图：左右排布
            (
                (x1, y1),
                (x1 + region_width//2 - spacing//2, y2),
                (x1 + region_width//2 + spacing//2, y1), (x2, y2),
                64
            )
            if is_vertical else
            # 横图：上下排布
            (
                (x1, y1), 
                (x2, y1 + (region_height - min(region_height//2, 100))),
                (x1, y1 + (region_height - min(region_height//2, 100)) + spacing), 
                (x2, y2), 
                64
            )
        )
        # 绘制图片
        img_segment = paste_image_auto(
            image_source=base_image_path,
            top_left=img_tl,
            bottom_right=img_br,
            content_image=pil_img,
            align="center",
            valign="middle",
            padding=12,
            allow_upscale=True,
            keep_alpha=True,
            image_overlay=None
        )
        # 绘制文本
        return draw_text_auto(
            image_source=io.BytesIO(img_segment),
            top_left=text_tl,
            bottom_right=text_br,
            text=text.strip(),
            color=(0, 0, 0),
            bracket_color=(106, 90, 205),
            max_font_height=text_font_height,
            font_path=fix_path(config.font_file),
            image_overlay=fix_path(config.base_overlay_file) if config.use_base_overlay else None
        )

# 注册命令处理函数
@anan.handle()
async def _(arg: Message = CommandArg()):
    try:
        # 解析消息
        text_args: List[str] = []
        image_url: Optional[str] = None
        for seg in arg:
            if seg.type == "text":
                text = seg.data.get("text", "").strip()
                if text:
                    text_args.extend(text.split())
            elif seg.type == "image" and not image_url:  # 只取第一张图片
                data = seg.data or {}
                image_url = data.get("url") or data.get("file") or data.get("image")
        # 获取差分
        processed_args, base_image_path = get_diff_info(text_args, bool(image_url))
        text_content = " ".join(processed_args).strip()
        # 处理包含图片的情况
        if image_url:
            img_bytes = await handle_image_content(image_url, base_image_path, text_content)
        else:
            # 绘制文本
            img_bytes = draw_text_auto(
                image_source=base_image_path,
                top_left=config.text_box_topleft,
                bottom_right=config.image_box_bottomright,
                text=text_content or usage, # 默认显示使用方法
                color=(0, 0, 0),
                bracket_color=(106, 90, 205),
                max_font_height=64,
                font_path=fix_path(config.font_file),
                image_overlay=fix_path(config.base_overlay_file) if config.use_base_overlay else None
            )
        b64 = base64.b64encode(img_bytes).decode()
        message = MessageSegment.image(f"base64://{b64}")
    except Exception as e:
        logger.exception(f"生成图片失败: {str(e)}")
        message = f"生成失败: {str(e)[:50]}"
    await anan.finish(message)

# 如果启用了convert_all_to_anan，尝试在Bot实例连接时hook其send方法
if getattr(config, "convert_all_to_anan", False):
    import re
    from types import MethodType
    from nonebot import get_driver

    _driver = get_driver()
    _patched_bots = set()
    # 在Bot实例连接时hook其send方法
    @_driver.on_bot_connect
    async def hook_anan_to_sender(bot):
        bot_id = bot.self_id
        if bot_id in _patched_bots: return
        _patched_bots.add(bot_id)
        _original_send = bot.send
        # 添加作画逻辑后的send方法
        async def anan_hooked_send(self, event=None, message=None, **kwargs):
            # 避免递归调用
            if kwargs.pop("_anan_skip", None):
                return await _original_send(event=event, message=message, **kwargs)
            # 过滤非Onebot文本消息
            if not isinstance(message, str) or not (raw := message.strip()):
                return await _original_send(event=event, message=message, **kwargs)
            # 过滤空消息和CQ码
            if not raw or not re.search(r"\[CQ:[^]]+]", raw, re.IGNORECASE):
                return await _original_send(event=event, message=message, **kwargs)
            try:
                # 绘制文本
                img_bytes = draw_text_auto(
                    image_source=fix_path(config.baseimage_mapping.get(None, config.baseimage_file)),
                    top_left=config.text_box_topleft,
                    bottom_right=config.image_box_bottomright,
                    text=raw,
                    color=(0, 0, 0),
                    bracket_color=(106, 90, 205),
                    max_font_height=64,
                    font_path=fix_path(config.font_file),
                    image_overlay=fix_path(config.base_overlay_file) if config.use_base_overlay else None,
                )
                b64 = base64.b64encode(img_bytes).decode()
                message = MessageSegment.image(f"base64://{b64}")
                kwargs["_anan_skip"] = True # 避免递归调用
            except Exception as e:
                logger.exception(f"安安自动转图失败: {e}")
            return await _original_send(event=event, message=message, **kwargs)
        bot.send = MethodType(anan_hooked_send, bot)
