"""NoneBot2 插件：Anan's Sketchbook

提供两个功能：
- /anan <text>：将文本绘制到默认底图并发送图片。
- 接收消息中的图片：将用户发送的图片粘贴到默认底图并发送图片。

依赖：nonebot2, nonebot-adapter-onebot, httpx, pillow
"""
from __future__ import annotations

import base64
import io
import logging
from typing import Optional

from nonebot import on_command, on_message
from nonebot.adapters.onebot.v11 import Bot, Event, MessageSegment
from nonebot.params import CommandArg

from PIL import Image

from config import Config
from image_fit_paste import paste_image_auto
from text_fit_draw import draw_text_auto

import httpx

logger = logging.getLogger(__name__)

config = Config()


anan = on_command("anan", aliases={"sketch"}, priority=5)


@anan.handle()
async def _(bot: Bot, event: Event, arg: MessageSegment = CommandArg()):
    """命令用法：/anan 文本

    将文本渲染到底图并发送图片（使用 `text_fit_draw.draw_text_auto`）。
    """
    text = arg.extract_plain_text().strip()
    if not text:
        await anan.finish("请在命令后输入要生成的文本，例如：/anan 你好世界")

    try:
        png_bytes = draw_text_auto(
            image_source=config.baseimage_file,
            top_left=config.text_box_topleft,
            bottom_right=config.image_box_bottomright,
            text=text,
            color=(0, 0, 0),
            max_font_height=64,
            font_path=config.font_file,
            image_overlay=(config.base_overlay_file if config.use_base_overlay else None),
        )
    except Exception as e:
        logger.exception("文本生成图片失败")
        await anan.finish(f"生成失败: {e}")

    b64 = base64.b64encode(png_bytes).decode()
    await anan.finish(MessageSegment.image(f"base64://{b64}"))


image_msg = on_message(priority=10)


@image_msg.handle()
async def handle_image_message(bot: Bot, event: Event):
    """当用户发送包含图片的消息时，自动把图片粘贴到底图并返回结果。

    该处理器会尝试读取消息中的第一个图片段，下载图片内容并用
    `image_fit_paste.paste_image_auto` 生成最终 PNG，再以 base64 发送。
    """
    segments = event.get_message()
    # 查找第一张图片段
    img_url: Optional[str] = None
    for seg in segments:
        if seg.type == "image":
            # 常见字段有: url, file, image
            data = getattr(seg, "data", {})
            if not isinstance(data, dict):
                data = {}
            img_url = data.get("url") or data.get("file") or data.get("image")
            break

    if not img_url:
        return  # 不是图片消息，忽略

    try:
        async with httpx.AsyncClient() as client:
            resp = await client.get(img_url, timeout=20.0)
            resp.raise_for_status()
            img_bytes = resp.content

        pil_img = Image.open(io.BytesIO(img_bytes)).convert("RGBA")

        png_bytes = paste_image_auto(
            image_source=config.baseimage_file,
            top_left=config.text_box_topleft,
            bottom_right=config.image_box_bottomright,
            content_image=pil_img,
            align="center",
            valign="middle",
            padding=12,
            allow_upscale=True,
            keep_alpha=True,
            image_overlay=(config.base_overlay_file if config.use_base_overlay else None),
        )

        b64 = base64.b64encode(png_bytes).decode()
        await image_msg.finish(MessageSegment.image(f"base64://{b64}"))

    except Exception as e:
        logger.exception("处理图片消息失败")
        # 不打断其他插件，记录并回复错误消息
        await image_msg.finish(f"生成图片失败: {e}")
