# waveshare-epd-image
A simple, no-boilerplate Python library for displaying images on Waveshare e-paper (EPD) displays.

Most Waveshare examples require copying scripts, editing driver code, and handling image conversion manually.
This library reduces all of that to a single function call

```python
from epd_image import display_image

display_image("image.png", mode="fit", rotation=90)
```
