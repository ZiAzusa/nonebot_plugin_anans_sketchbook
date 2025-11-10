from pydantic import BaseModel

# 本文件中包含了各种参数, 可以进行调整
# 其中以"#"开头的注释为说明该参数的使用方法

# 生成图片的热键, 用于 keyboard 库
# 【格式】
#    1. 单键：直接写键名，如：
#         "enter"、"space"、"esc"、"tab"、"f5"、"backspace"
#    2. 组合键：多个键用加号连接（不区分大小写），如：
#         "ctrl+s"、"ctrl+shift+g"、"alt+enter"
#    3. 连续热键（序列触发）：使用逗号分隔表示按键顺序，如：
#         "ctrl+s, ctrl+shift+s"   → 表示先按 Ctrl+S，再按 Ctrl+Shift+S
#    4. 不区分大小写：'Ctrl+S' 与 'ctrl+s' 等价。
#    5. 修饰键在前，主键在后：'ctrl+alt+p'、'shift+enter'，可同时包含多个修饰符。
#
# 【常见键名示例】
#    - 字母数字键：'a' ~ 'z'、'0' ~ '9'
#    - 功能键：'f1' ~ 'f12'
#    - 修饰键：'ctrl'、'alt'、'shift'、'windows'
#    - 控制键：'enter'、'space'、'tab'、'backspace'、'delete'、'esc'
#    - 方向键：'up'、'down'、'left'、'right'
HOTKEY = "enter"

# 允许运行此程序的进程列表，只有当前最上层窗口属于这些进程时，热键才会生效
# 例如: ["qq.exe", "weixin.exe"] 表示只在QQ和微信中生效
# 留空列表 [] 表示在所有进程中生效
# 此值为字符串列表
ALLOWED_PROCESSES = ["qq.exe", "weixin.exe"]

# 全选快捷键, 此按键并不会监听, 而是会作为模拟输入
# 此值为字符串, 代表热键的键名, 格式同 HOTKEY
SELECT_ALL_HOTKEY = "ctrl+a"

# 剪切快捷键, 此按键并不会监听, 而是会作为模拟输入
# 此值为字符串, 代表热键的键名, 格式同 HOTKEY
CUT_HOTKEY = "ctrl+x"

# 黏贴快捷键, 此按键并不会监听, 而是会作为模拟输入
# 此值为字符串, 代表热键的键名, 格式同 HOTKEY
PASTE_HOTKEY = "ctrl+v"

# 发送消息快捷键, 此按键并不会监听, 而是会作为模拟输入
# 此值为字符串, 代表热键的键名, 格式同 HOTKEY
SEND_HOTKEY = "enter"

# 是否阻塞按键, 如果热键设置为阻塞模式, 则按下热键时不会将该按键传递给前台应用
# 如果生成热键和发送热键相同, 则强制阻塞, 防止误触发发送消息
# 此值为布尔值, True 或 False
BLOCK_HOTKEY = False

# 操作的间隔, 如果失效可以适当增大此数值
# 此值为数字, 单位为秒
DELAY = 0.1

# 使用字体的文件名, 需要自己导入
# 此值为字符串, 代表相对main的相对路径
FONT_FILE = "font.ttf"

# 将差分表情导入，默认底图base.png
# 使用底图的文件名, 需要自己导入
# 此值为字符串, 代表相对main的相对路径
BASEIMAGE_MAPPING = {
    "#普通#": "BaseImages\\base.png",
    "#开心#": "BaseImages\\开心.png",
    "#生气#": "BaseImages\\生气.png",
    "#无语#": "BaseImages\\无语.png",
    "#脸红#": "BaseImages\\脸红.png",
    "#病娇#": "BaseImages\\病娇.png",
}
BASEIMAGE_FILE = "BaseImages\\base.png"

# 文本框左上角坐标 (x, y), 同时适用于图片框
# 此值为一个二元组, 例如 (100, 150), 单位像素, 图片的左上角记为 (0, 0)
TEXT_BOX_TOPLEFT = (119, 450)

# 文本框右下角坐标 (x, y), 同时适用于图片框
# 此值为一个二元组, 例如 (100, 150), 单位像素, 图片的左上角记为 (0, 0)
IMAGE_BOX_BOTTOMRIGHT = (119 + 279, 450 + 175)

# 置顶图层的文件名, 需要自己导入
# 此值为字符串, 代表相对main的相对路径
BASE_OVERLAY_FILE = "BaseImages\\base_overlay.png"

# 是否启用底图的置顶图层, 用于表现遮挡
# 此值为布尔值, True 或 False
USE_BASE_OVERLAY = True

# 是否自动黏贴生成的图片(如果为否则保留图片在剪贴板, 可以手动黏贴)
# 此值为布尔值, True 或 False
AUTO_PASTE_IMAGE = True

# 生成图片后是否自动发送(模拟回车键输入), 只有开启自动黏贴才生效
# 此值为布尔值, True 或 False
AUTO_SEND_IMAGE = True

# 日志记录等级, 可选值有 "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"
# 此值为字符串
LOGGING_LEVEL = "INFO"


class Config(BaseModel):
    hotkey: str = HOTKEY
    """全局热键, 用于 keyboard 库"""
    allowed_processes: list[str] = ALLOWED_PROCESSES
    """允许的进程列表"""
    select_all_hotkey: str = SELECT_ALL_HOTKEY
    """全选快捷键"""
    cut_hotkey: str = CUT_HOTKEY
    """剪切快捷键"""
    paste_hotkey: str = PASTE_HOTKEY
    """黏贴快捷键"""
    send_hotkey: str = SEND_HOTKEY
    """发送消息快捷键"""
    block_hotkey: bool = BLOCK_HOTKEY
    """阻塞热键"""
    delay: float = DELAY
    """操作延时（秒）"""
    font_file: str = FONT_FILE
    """字体文件路径"""
    baseimage_mapping: dict[str, str] = BASEIMAGE_MAPPING
    """差分表情映射字典"""
    baseimage_file: str = BASEIMAGE_FILE
    """默认底图文件路径"""
    text_box_topleft: tuple[int, int] = TEXT_BOX_TOPLEFT
    """文本框左上角坐标"""
    image_box_bottomright: tuple[int, int] = IMAGE_BOX_BOTTOMRIGHT
    """文本框右下角坐标"""
    base_overlay_file: str = BASE_OVERLAY_FILE
    """底图置顶图层文件路径"""
    use_base_overlay: bool = USE_BASE_OVERLAY
    """是否使用底图置顶图层"""
    auto_paste_image: bool = AUTO_PASTE_IMAGE
    """是否自动黏贴图片"""
    auto_send_image: bool = AUTO_SEND_IMAGE
    """是否自动发送图片"""
    logging_level: str = LOGGING_LEVEL
    """日志记录等级"""
