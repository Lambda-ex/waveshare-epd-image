import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from epd_image import display_image

print("Displaying image on EPD...") #
display_image("vertical.png", mode="fill", rotation=0, model="epd5in65f", refresh=True)