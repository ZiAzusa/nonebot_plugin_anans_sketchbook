import yaml
from pathlib import Path
from pydantic import BaseModel, Field
from typing import Union

class Config(BaseModel):
    font_file: str = Field("resources/font.ttf", description="使用字体的文件路径")
    baseimage_mapping: dict[str, str] = Field(
        {
            "普通": "resources/BaseImages/base.png",
            "开心": "resources/BaseImages/开心.png",
            "生气": "resources/BaseImages/生气.png",
            "无语": "resources/BaseImages/无语.png",
            "脸红": "resources/BaseImages/脸红.png",
            "病娇": "resources/BaseImages/病娇.png",
        },
        description="将差分表情导入，默认底图base.png",
    )
    baseimage_file: str = Field("resources/BaseImages/base.png", description="默认底图文件路径")
    text_box_topleft: tuple[int, int] = Field((119, 450), description="文本框左上角坐标 (x, y), 同时适用于图片框")
    image_box_bottomright: tuple[int, int] = Field(
        (119 + 279, 450 + 175), description="文本框右下角坐标 (x, y), 同时适用于图片框"
    )
    base_overlay_file: str = Field(
        "resources/BaseImages/base_overlay.png", description="置顶图层的文件路径"
    )
    use_base_overlay: bool = Field(True, description="是否启用底图的置顶图层, 用于表现遮挡")
    logging_level: str = Field("INFO", description="日志记录等级, 可选值有 \"DEBUG\", \"INFO\", \"WARNING\", \"ERROR\", \"CRITICAL\"")

    @classmethod
    def load(cls, path: Union[str, Path] = "config.yaml") -> "Config":
        path = path = Path(__file__).parent.parent / path
        if not path.exists():
            print(f"[Config] 未找到 {path}，正在创建默认配置...")
            default_cfg = cls()
            with path.open("w", encoding="utf-8") as f:
                yaml.safe_dump(default_cfg.dict(), f, allow_unicode=True, sort_keys=False)
            return default_cfg

        with path.open("r", encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}

        # 处理坐标值，确保它们是元组而不是列表
        if 'text_box_topleft' in data and isinstance(data['text_box_topleft'], list):
            data['text_box_topleft'] = tuple(data['text_box_topleft'])
    
        if 'image_box_bottomright' in data and isinstance(data['image_box_bottomright'], list):
            data['image_box_bottomright'] = tuple(data['image_box_bottomright'])

        return cls(**data)
