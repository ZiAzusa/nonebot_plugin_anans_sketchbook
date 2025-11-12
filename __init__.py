from __future__ import annotations

import base64
import io
import logging
from typing import Optional, List

from nonebot import on_command
from nonebot.adapters.onebot.v11 import Bot, Event, MessageSegment, Message
from nonebot.params import CommandArg

from PIL import Image
import httpx

from .image_fit_paste import paste_image_auto
from .text_fit_draw import draw_text_auto
from .config import Config

config = Config.load()

logger = logging.getLogger(__name__)


# 命令触发器：支持 /anan 与 夏目安安
anan = on_command("anan", aliases={"夏目安安"}, priority=5)


@anan.handle()
async def _(bot: Bot, event: Event, arg: Message = CommandArg()):
    """
    命令用法：
    - 夏目安安 文本：生成文字图
    - 夏目安安 开心 文本：切换到“开心”差分底图后生成文字图
    - 夏目安安 开心 [CQ:image...]：切换差分底图后合成图片
    """
    try:
        # 提取消息段
        segments = arg
        text_args: List[str] = []
        image_url: Optional[str] = None

        for seg in segments:
            if seg.type == "text":
                # 分词并清除多余空格
                text_args.extend(seg.data.get("text", "").strip().split())
            elif seg.type == "image":
                data = getattr(seg, "data", {})
                if not isinstance(data, dict):
                    data = {}
                image_url = data.get("url") or data.get("file") or data.get("image")

        # 优先处理图片
        if image_url:
            await handle_image(bot, event, image_url, text_args)
            return

        # 没有图片 → 文字生成
        if not text_args:
            await anan.finish("请在命令后输入要生成的文本，例如：夏目安安 你好世界")

        # 差分判断（自动支持带#或不带#）
        diff = None
        first_arg = text_args[0]
        diff_keys = list(config.baseimage_mapping.keys())
        normalized_keys = {k.strip("#"): k for k in diff_keys}

        if len(text_args) >= 2:
            if first_arg in diff_keys:
                diff = first_arg
                text_args.pop(0)
            elif first_arg in normalized_keys:
                diff = normalized_keys[first_arg]
                text_args.pop(0)

        # 拼接文本
        text = " ".join(text_args).strip()

        # 选择底图
        base_image = config.baseimage_mapping.get(diff, config.baseimage_file)

        # 绘制文字图
        png_bytes = draw_text_auto(
            image_source=base_image,
            top_left=config.text_box_topleft,
            bottom_right=config.image_box_bottomright,
            text=text,
            color=(0, 0, 0),
            max_font_height=64,
            font_path=config.font_file,
            image_overlay=(config.base_overlay_file if config.use_base_overlay else None),
        )

        b64 = base64.b64encode(png_bytes).decode()
        await anan.finish(MessageSegment.image(f"base64://{b64}"))

    except Exception as e:
        logger.exception("文本生成图片失败")
        await anan.finish(f"生成失败: {e}")


async def handle_image(bot: Bot, event: Event, img_url: str, args: List[str]):
    """处理图片合成功能（夏目安安 差分? [CQ:image...]）"""
    try:
        # 差分判断
        diff = None
        diff_keys = list(config.baseimage_mapping.keys())
        normalized_keys = {k.strip("#"): k for k in diff_keys}

        if args:
            first_arg = args[0]
            if first_arg in diff_keys:
                diff = first_arg
            elif first_arg in normalized_keys:
                diff = normalized_keys[first_arg]

        base_image = config.baseimage_mapping.get(diff, config.baseimage_file)

        # 下载图片
        async with httpx.AsyncClient() as client:
            resp = await client.get(img_url, timeout=20.0)
            resp.raise_for_status()
            img_bytes = resp.content

        pil_img = Image.open(io.BytesIO(img_bytes)).convert("RGBA")

        # 合成图片
        png_bytes = paste_image_auto(
            image_source=base_image,
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
        await anan.finish(MessageSegment.image(f"base64://{b64}"))

    except Exception as e:
        logger.exception("处理图片消息失败")
        await anan.finish(f"生成图片失败: {e}")
