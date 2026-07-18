import os
import inspect
import importlib
from typing import Optional, Literal

from PIL import Image

from .image import transform_image, prepare_for_epd, split_tricolor

Mode = Literal["fit", "fill", "stretch"]
Rotation = Literal[0, 90, 180, 270]

def _load_driver(model: str):
    """
    Dynamically import a driver module by name.

    model="epd2in13" -> epd_image.drivers.epd2in13
    """
    try:
        return importlib.import_module(f"epd_image.drivers.{model}")
    except ModuleNotFoundError as e:
        raise ValueError(
            f"Unknown EPD model '{model}'. Expected a module in epd_image/drivers named '{model}.py'."
        ) from e


def _get_dimensions(driver_module, epd_obj=None):
    # Prefer module constants if present (your example)
    w = getattr(driver_module, "EPD_WIDTH", None)
    h = getattr(driver_module, "EPD_HEIGHT", None)

    # Fallback to object attributes (some drivers use these)
    if (w is None or h is None) and epd_obj is not None:
        w = w or getattr(epd_obj, "width", None)
        h = h or getattr(epd_obj, "height", None)

    if w is None or h is None:
        raise RuntimeError("Could not determine display dimensions from driver.")
    return int(w), int(h)


def _required_positional_params(func):
    """Names of positional parameters without defaults, or None if uninspectable."""
    try:
        sig = inspect.signature(func)
    except (TypeError, ValueError):
        return None
    return [
        p.name
        for p in sig.parameters.values()
        if p.kind in (p.POSITIONAL_ONLY, p.POSITIONAL_OR_KEYWORD) and p.default is p.empty
    ]


def _is_tricolor(epd) -> bool:
    """
    Tri-color ("b"/"bc") drivers take two buffers: display(imageblack, imagered).
    Detect them by the arity of display().
    """
    display = getattr(epd, "display", None)
    if display is None:
        return False
    required = _required_positional_params(display)
    return required is not None and len(required) >= 2


def _sleep_epd(epd):
    """Put the panel to sleep (drivers name it sleep() or Sleep())."""
    sleep = getattr(epd, "sleep", None) or getattr(epd, "Sleep", None)
    if sleep is None:
        return
    try:
        sleep()
    except Exception:
        # Sleeping is a best-effort safety measure; never mask the original error.
        pass


def display_image(
    path: str,
    mode: Mode = "fit",
    rotation: Rotation = 0,
    model: Optional[str] = None,
    refresh: bool = True,
    scale: float = 1.0,
):
    """
    Display an image on a Waveshare EPD.

    - model: driver module name (e.g. "epd2in13"). If None, uses env var EPD_MODEL.
    - mode: "fit" | "fill" | "stretch"
    - rotation: 0 | 90 | 180 | 270 (clockwise)
    - refresh: if True, fully clears the panel before drawing (reduces ghosting).
      Disable to skip the clear pass and update faster.
    - scale: render the image at this fraction of the panel (0-1], centered
      with white margins. Useful when a physical frame covers the panel edges.

    The panel is always put to sleep afterwards, even on error, to avoid
    leaving it under high voltage.
    """
    model = model or os.getenv("EPD_MODEL")
    if not model:
        raise ValueError("EPD model not specified. Set EPD_MODEL or pass model='epd2in13'.")

    if rotation not in (0, 90, 180, 270):
        raise ValueError("rotation must be one of: 0, 90, 180, 270")

    driver = _load_driver(model)

    epd_class = getattr(driver, "EPD", None)
    if epd_class is None:
        raise RuntimeError(f"Driver '{model}' does not define an EPD class.")
    epd = epd_class()

    try:
        # Typical waveshare init pattern; wrap so missing methods don't explode silently
        if hasattr(epd, "init"):
            epd.init()

        width, height = _get_dimensions(driver, epd)

        # Load + transform
        with Image.open(path) as src:
            img = transform_image(src, width, height, mode=mode, rotation=rotation, scale=scale)
            img.load()

        if refresh:
            clear = getattr(epd, "Clear", None)
            # Only call Clear() when it works without arguments (signatures vary).
            if clear is not None and _required_positional_params(clear) == []:
                clear()

        if _is_tricolor(epd):
            # Tri-color panels take separate black and red/yellow planes.
            black_img, ry_img = split_tricolor(img)
            if hasattr(epd, "getbuffer"):
                epd.display(epd.getbuffer(black_img), epd.getbuffer(ry_img))
            else:
                epd.display(black_img, ry_img)
        else:
            # Convert to the best format for this display
            img = prepare_for_epd(img, driver_module=driver, epd_obj=epd)

            # Display: waveshare drivers vary (display / display_Base / getbuffer)
            if hasattr(epd, "getbuffer"):
                buf = epd.getbuffer(img)
                if hasattr(epd, "display"):
                    epd.display(buf)
                else:
                    raise RuntimeError("EPD object has getbuffer() but no display() method.")
            elif hasattr(epd, "display"):
                epd.display(img)  # some drivers accept PIL directly
            else:
                raise RuntimeError("Unsupported driver API: expected display() and possibly getbuffer().")
    finally:
        _sleep_epd(epd)

    return True
