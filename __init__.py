from __future__ import annotations

import base64
import io
import logging
from typing import Optional, List, Tuple
from pathlib import Path

from PIL import Image
import httpx

from nonebot import on_command
from nonebot.adapters.onebot.v11 import Bot, Event, MessageSegment, Message
from nonebot.params import CommandArg
from nonebot.exception import FinishedException

from .utils.image_fit_paste import paste_image_auto
from .utils.text_fit_draw import draw_text_auto
from .utils.config import Config

config = Config.load()
logger = logging.getLogger(__name__)
PLUGIN_DIR = str(Path(__file__).parent) + "/"

usage = f"""\
命令：anan 或 夏目安安
功能：生成夏目安安的素描本聊天框
支持的差分表情：{', '.join(config.baseimage_mapping.keys())}

用法：夏目安安 ?可选差分 文本/图片（优先图片）

例如：夏目安安 开心 这是吾辈在【说话】
"""

# 命令触发器
anan = on_command("anan", aliases={"夏目安安"}, priority=5)

# 切到插件目录
def fix_path(filename: str) -> str:
    return PLUGIN_DIR + filename

# 根据参数列表获取处理后的参数列表和底图路径
def get_diff_info(args: List[str]) -> Tuple[Optional[str], List[str], str]:
    if not args:
        # 无参数时使用默认底图
        default_image = config.baseimage_mapping.get(None, config.baseimage_file)
        return args, fix_path(default_image)
    
    diff_keys = config.baseimage_mapping.keys()
    if args[0] in diff_keys:
        # 匹配到差分，返回对应底图
        diff_image = config.baseimage_mapping[args[0]]
        return args[1:], fix_path(diff_image)
    else:
        # 未匹配到差分，使用默认底图
        default_image = config.baseimage_mapping.get(None, config.baseimage_file)
        return args, fix_path(default_image)

@anan.handle()
async def _(arg: Message = CommandArg()):
    try:
        # 解析消息：分离文本参数和图片URL
        text_args: List[str] = []
        image_url: Optional[str] = None
        for seg in arg:
            if seg.type == "text":
                text = seg.data.get("text", "").strip()
                if text:
                    text_args.extend(text.split())
            elif seg.type == "image" and not image_url:  # 只取第一张图片
                data = getattr(seg, "data", {}) or {}
                image_url = data.get("url") or data.get("file") or data.get("image")
 
        processed_args, base_image_path = get_diff_info(text_args)

        if image_url:
            await handle_image(image_url, base_image_path)
            return

        # 写入文本并发送
        text_image = draw_text_auto(
            image_source=base_image_path,
            top_left=config.text_box_topleft,
            bottom_right=config.image_box_bottomright,
            text=" ".join(processed_args) if processed_args else usage, # 默认显示使用方法
            color=(0, 0, 0),
            bracket_color=(106, 90, 205),
            max_font_height=64,
            font_path=fix_path(config.font_file),
            image_overlay=fix_path(config.base_overlay_file) if config.use_base_overlay else None,
        )
        b64 = base64.b64encode(text_image).decode()
        await anan.finish(MessageSegment.image(f"base64://{b64}"))

    except FinishedException:
        return
    except Exception as e:
        logger.exception(f"生成图片失败: {str(e)}")
        await anan.finish(f"生成失败: {str(e)[:50]}")

async def handle_image(img_url: str, base_image_path: str):
    try:
        # 下载图片
        async with httpx.AsyncClient() as client:
            resp = await client.get(img_url, timeout=20.0)
            resp.raise_for_status()

        # 写入图片并发送
        with Image.open(io.BytesIO(resp.content)).convert("RGBA") as pil_img:
            combined_image = paste_image_auto(
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
        b64 = base64.b64encode(combined_image).decode()
        await anan.finish(MessageSegment.image(f"base64://{b64}"))

    except FinishedException:
        return
    except Exception as e:
        logger.exception(f"生成图片失败: {str(e)}")
        await anan.finish(f"生成图片失败: {str(e)[:50]}")