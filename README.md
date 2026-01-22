# waveshare-epd-image
**Version:** 0.5.0  
**Status:** Functional

A simple, no-boilerplate Python library for displaying images on Waveshare e-paper (EPD) displays using a Raspberry Pi and GPIO.

Most Waveshare examples require copying scripts, editing driver code, and handling image conversion manually.
This library reduces all of that to a single function call.

```python
from epd_image import display_image

# Display Image (pass display model/driver name)
display_image("image.png", mode="fit", model="epd5in65f", rotation=90)

# Skip refresh (optional)
display_image("image.png", mode="fit", model="epd5in65f", rotation=90, refresh=False)
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
Follow instructions on the Waveshare EPD documentation for wiring.

Install the function library:  
```
sudo apt-get update
sudo apt-get install python3-pip
sudo apt-get install python3-pil
sudo apt-get install python3-numpy
sudo apt-get install python3-spidev
```

pip install (need more details here to install the library!)

Run the demo

# Additional Notes & Developer Words
- This project is ongoing. Though this has worked with my personal hardware, I not certain it will run on yours. Theoretically it should though!
- This is my first public repository, be kind but do offer productive criticism if needed.

I love Waveshares EPD. I believe e-paper is an elegant way to display computer graphics. I found myself writing a few programs for the display, and ran into an issue. There were so many helper functions and scripts I was writing, it was becoming overwhelming to write one for each project.  
My regular workflow would be to create an image I'd want to display (weather, calendar, a clock) then send it to the EPD. However due to repeated code, I saw an opporitunity. How great would it be to just import a library that does all the work?

Displaying an image wasn't as easy as I thought. Questions arose such as:  
- What happens when an image is too large or small for the display? 
- Why shouldn't I be able to simply rotate the image if the display is portrait?
- What if I wanted to display a portrait image on a landscape display?  

I found it fascinating that there could potentially be an algoritm that would solve these issues, and there was! Given an input image and the resolution of the display, you can calculate how to fit it given three simple configurations: Fit, Fill, Stretch. Sound familiar? I remember seeing the same three configs when setting my desktop background in Windows. I couldn't find the original author, but kudos to them! Performing these operations taking into account the rotation of the image displays it nicely.  
Given an EPD display model, I can pull the resolution from the Waveshare drivers, run the algorithm to fit the image, and display it. Boom. I have solved my issue of wanting to show an image on a screen.  
Hopefully I can continue using this library for future projects, and more importantly, people will find it useful for themselves as well. This is my first official public personal project and to say the least I am very proud.

# Credit & Attribution

This project is not affiliated with or endorsed by Waveshare.

Waveshare® is a registered trademark of Waveshare Electronics.  
This library is an independent, open-source project designed to simplify image display on Waveshare e-paper (EPD) displays using a Raspbery Pi.
