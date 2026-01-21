# waveshare-epd-image
**Version:** 0.0  
**Status:** Early development

A simple, no-boilerplate Python library for displaying images on Waveshare e-paper (EPD) displays.

Most Waveshare examples require copying scripts, editing driver code, and handling image conversion manually.
This library reduces all of that to a single function call.

```python
from epd_image import display_image

# Your display model here
init_epd("epd5in65f")

# Display
display_image("image.png", mode="fit", rotation=90)

# Skip refresh (optional)
display_image("image.png", mode="fit", rotation=90, refresh=false)
```

## Supported Input Image Formats
| Image Format | Supported |
|-------------|-----------|
| PNG         | ✅ Yes    |
| JPEG / JPG  | ✅ Yes    |
| BMP         | ✅ Yes    |
| GIF         | ⚠️ Static only |
| TIFF        | ❌ No     |
| WEBP        | ❌ No     |

## Display Modes
| Mode        | Description                                                                                                       |
| ----------- | ----------------------------------------------------------------------------------------------------------------- |
| **fit**     | Scales the image to fit within the display while preserving aspect ratio. Empty space may appear on the sides.    |
| **fill**    | Scales the image to completely fill the display while preserving aspect ratio. Parts of the image may be cropped. |
| **stretch** | Stretches the image to exactly match the display size. Aspect ratio is not preserved.                             |

## Rotation
| Value | Description           |
| ----: | --------------------- |
|   `0` | No rotation (default) |
|  `90` | Rotate 90° clockwise  |
| `180` | Rotate 180°           |
| `270` | Rotate 270° clockwise |

## Refresh
To save battery and/or RAM, or to speed up the displaying process, disable `refresh`.
