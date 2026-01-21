from PIL import Image
from typing import Literal

Mode = Literal["fit", "fill", "stretch"]

def transform_image(img: Image.Image, width: int, height: int, mode: Mode, rotation: int) -> Image.Image:
    # Ensure consistent orientation first
    if rotation:
        img = img.rotate(-rotation, expand=True)  # PIL rotate is CCW; negative makes it clockwise

    if mode == "stretch":
        return img.resize((width, height), Image.LANCZOS)

    # Preserve aspect ratio for fit/fill
    src_w, src_h = img.size
    src_ratio = src_w / src_h
    dst_ratio = width / height

    if mode == "fit":
        if src_ratio > dst_ratio:
            new_w = width
            new_h = int(round(width / src_ratio))
        else:
            new_h = height
            new_w = int(round(height * src_ratio))
        resized = img.resize((new_w, new_h), Image.LANCZOS)

        # Letterbox/pad to exact size (centered)
        canvas = Image.new("RGB", (width, height), color=(255, 255, 255))
        x = (width - new_w) // 2
        y = (height - new_h) // 2
        canvas.paste(resized, (x, y))
        return canvas

    if mode == "fill":
        if src_ratio > dst_ratio:
            # wider than target -> scale by height and crop width
            new_h = height
            new_w = int(round(height * src_ratio))
        else:
            # taller than target -> scale by width and crop height
            new_w = width
            new_h = int(round(width / src_ratio))
        resized = img.resize((new_w, new_h), Image.LANCZOS)

        # Center crop
        left = (new_w - width) // 2
        top = (new_h - height) // 2
        right = left + width
        bottom = top + height
        return resized.crop((left, top, right, bottom))

    raise ValueError("mode must be one of: fit, fill, stretch")

def epd_supports_color(epd_obj) -> bool:
    """
    Heuristic: Waveshare mono drivers typically expose BLACK/WHITE only.
    Color drivers expose additional named colors (RED/YELLOW/ORANGE/etc).
    """
    if epd_obj is None:
        return False

    # Most common mono: BLACK + WHITE only
    has_black = hasattr(epd_obj, "BLACK")
    has_white = hasattr(epd_obj, "WHITE")

    # Color panels typically add at least one of these
    extra_color_attrs = ("RED", "YELLOW", "ORANGE", "GREEN", "BLUE")

    has_extra = any(hasattr(epd_obj, a) for a in extra_color_attrs)

    return has_black and has_white and has_extra

def prepare_for_epd(img: Image.Image, driver_module, epd_obj=None) -> Image.Image:
    """
    Convert to a reasonable image mode for the target display.

    Many mono EPDs prefer 1-bit ('1'). Color panels vary.
    This keeps it simple and defaults to mono unless we can detect color support.
    """
    has_color = epd_supports_color(epd_obj)

    if has_color:
        return img.convert("RGB")
    return img.convert("1")
