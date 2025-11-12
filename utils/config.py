import yaml
from pathlib import Path
from pydantic import BaseModel, Field
from typing import Union

class Config(BaseModel):
    font_file: str = Field("sources/font.ttf", description="字体文件路径")
    baseimage_mapping: dict[str, str] = Field(
        {
            "普通": "sources/BaseImages/base.png",
            "开心": "sources/BaseImages/开心.png",
            "生气": "sources/BaseImages/生气.png",
            "无语": "sources/BaseImages/无语.png",
            "脸红": "sources/BaseImages/脸红.png",
            "病娇": "sources/BaseImages/病娇.png",
        },
        description="差分表情映射字典",
    )
    baseimage_file: str = Field("sources/BaseImages/base.png", description="默认底图文件路径")
    text_box_topleft: tuple[int, int] = Field((119, 450), description="文本框左上角坐标")
    image_box_bottomright: tuple[int, int] = Field(
        (119 + 279, 450 + 175), description="文本框右下角坐标"
    )
    base_overlay_file: str = Field(
        "sources/BaseImages/base_overlay.png", description="底图置顶图层文件路径"
    )
    use_base_overlay: bool = Field(True, description="是否使用底图置顶图层")
    delay: float = Field(0.1, description="生成图片操作延时（秒）")
    logging_level: str = Field("INFO", description="日志记录等级")

    @classmethod
    def load(cls, path: Union[str, Path] = "config.yaml") -> "Config":
        path = Path(str(Path(__file__).parent.parent)+"/"+path)
        if not path.exists():
            print(f"[Config] 未找到 {path}，正在创建默认配置...")
            default_cfg = cls()
            with path.open("w", encoding="utf-8") as f:
                yaml.safe_dump(default_cfg.dict(), f, allow_unicode=True, sort_keys=False)
            return default_cfg

        with path.open("r", encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}
        return cls(**data)
