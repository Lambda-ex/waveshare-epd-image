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


def prepare_for_epd(img: Image.Image, driver_module, epd_obj=None) -> Image.Image:
    """
    Convert to a reasonable image mode for the target display.

    Many mono EPDs prefer 1-bit ('1'). Color panels vary.
    This keeps it simple and defaults to mono unless we can detect color support.
    """
    # Try to infer color capability (you can refine later)
    has_color = False
    for attr in ("is_color", "has_color", "color"):
        if hasattr(epd_obj, attr) and bool(getattr(epd_obj, attr)):
            has_color = True

    # Some driver modules define constants like EPD_COLOR, etc. (not always)
    if hasattr(driver_module, "EPD_COLOR"):
        has_color = True

    if has_color:
        # Keep color; drivers often accept RGB and do their own quantization
        return img.convert("RGB")
    else:
        # Monochrome: convert to 1-bit with dithering
        return img.convert("1")
