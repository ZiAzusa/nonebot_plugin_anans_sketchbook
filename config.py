import yaml
from pathlib import Path
from pydantic import BaseModel, Field


class Config(BaseModel):
    """NoneBot 环境下的 YAML 配置"""

    font_file: str = Field("font.ttf", description="字体文件路径")
    baseimage_mapping: dict[str, str] = Field(
        {
            "普通": "BaseImages/base.png",
            "开心": "BaseImages/开心.png",
            "生气": "BaseImages/生气.png",
            "无语": "BaseImages/无语.png",
            "脸红": "BaseImages/脸红.png",
            "病娇": "BaseImages/病娇.png",
        },
        description="差分表情映射字典",
    )
    baseimage_file: str = Field("BaseImages/base.png", description="默认底图文件路径")
    text_box_topleft: tuple[int, int] = Field((119, 450), description="文本框左上角坐标")
    image_box_bottomright: tuple[int, int] = Field(
        (119 + 279, 450 + 175), description="文本框右下角坐标"
    )
    base_overlay_file: str = Field(
        "BaseImages/base_overlay.png", description="底图置顶图层文件路径"
    )
    use_base_overlay: bool = Field(True, description="是否使用底图置顶图层")
    delay: float = Field(0.1, description="生成图片操作延时（秒）")
    logging_level: str = Field("INFO", description="日志记录等级")

    @classmethod
    def load(cls, path: str | Path = "config.yaml") -> "Config":
        """加载配置文件，如不存在则创建默认配置"""
        path = Path(path)
        if not path.exists():
            print(f"[Config] 未找到 {path}，正在创建默认配置...")
            default_cfg = cls()
            with path.open("w", encoding="utf-8") as f:
                yaml.safe_dump(default_cfg.model_dump(), f, allow_unicode=True, sort_keys=False)
            return default_cfg

        with path.open("r", encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}
        return cls(**data)
