# waveshare-epd-image
**Version:** 0.1
**Status:** Functional

A simple, no-boilerplate Python library for displaying images on Waveshare e-paper (EPD) displays using a Raspberry Pi and GPIO.

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
**Note:** Color rendering automatically matches the capabilities of the display.  
Color-capable displays will render color images; monochrome displays will not.

## Platform Support

This library is designed to run on Linux-based systems with SPI support,
such as the Raspberry Pi.

It is not intended for use on Windows or macOS.

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

# Install Instructions
(Instructions here regarding setup)

# Credit & Attribution

This project is not affiliated with or endorsed by Waveshare.

Waveshare® is a registered trademark of Waveshare Electronics.  
This library is an independent, open-source project designed to simplify image display on Waveshare e-paper (EPD) displays using a Raspbery Pi.
