import os
import importlib
from typing import Optional, Literal

from PIL import Image

from .image import transform_image, prepare_for_epd

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


def display_image(
    path: str,
    mode: Mode = "fit",
    rotation: Rotation = 0,
    model: Optional[str] = None,
    refresh: bool = True,
):
    """
    Display an image on a Waveshare EPD.

    - model: driver module name (e.g. "epd2in13"). If None, uses env var EPD_MODEL.
    - mode: "fit" | "fill" | "stretch"
    - rotation: 0 | 90 | 180 | 270 (clockwise)
    - refresh: if True, triggers a panel refresh after updating
    """
    model = model or os.getenv("EPD_MODEL")
    if not model:
        raise ValueError("EPD model not specified. Set EPD_MODEL or pass model='epd2in13'.")

    if rotation not in (0, 90, 180, 270):
        raise ValueError("rotation must be one of: 0, 90, 180, 270")

    driver = _load_driver(model)

    # Instantiate and initialize EPD (naming varies across driver sets)
    epd = getattr(driver, "EPD", None)
    if epd is None:
        raise RuntimeError(f"Driver '{model}' does not define an EPD class.")
    epd = epd()

    # Typical waveshare init pattern; wrap so missing methods don't explode silently
    if hasattr(epd, "init"):
        epd.init()

    width, height = _get_dimensions(driver, epd)

    # Load + transform
    img = Image.open(path)
    img = transform_image(img, width, height, mode=mode, rotation=rotation)

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

    if refresh:
        # Some drivers use epd.sleep(), some have epd.Clear(), etc.
        # There often isn't a separate refresh method; display() triggers it.
        # Leave this hook here for future partial-update/batching behavior.
        pass

    return True