from __future__ import annotations

from functools import lru_cache
from PIL import Image, ImageFont
import os

# 图片缓存
@lru_cache(maxsize=None)
def _cached_open_image(path: str):
    return Image.open(path).convert("RGBA")

def open_image(path=None):
    if isinstance(path, str) and os.path.isfile(path):
        return _cached_open_image(path).copy()
    return Image.open(path).copy()

# 字体缓存
@lru_cache(maxsize=None)
def _cached_truetype(path: str, size: int):
    return ImageFont.truetype(path, size=size)

@lru_cache(maxsize=None)
def _cached_default_font(size: int):
    try:
        return ImageFont.truetype("DejaVuSans.ttf", size=size)
    except Exception:
        return ImageFont.load_default()

def open_font(path=None, size=0):
    if path and isinstance(path, str) and os.path.isfile(path):
        return _cached_truetype(path, size)
    return _cached_default_font(size)