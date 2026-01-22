from epd_image import display_image

print("Displaying image on EPD...")
display_image("vertical.png", mode="fill", rotation=0, model="epd5in65f", refresh=True)