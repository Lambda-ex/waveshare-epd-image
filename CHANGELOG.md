# Changelog

All notable changes to this project will be documented in this file.

## [0.7.0] - 2026-07-18
### Added
- `scale` parameter: render the image at a fraction of the panel, centered
  with white margins (for frames/bezels that cover the panel edges)

## [0.6.1] - 2026-07-18
### Fixed
- Packaging: bundle the driver `.so` files in the wheel so pip installs include them

## [0.6.0] - 2026-07-18
### Added
- Tri-color ("b"/"bc") panel support: images are split into black and red/yellow planes automatically
- `.gitignore`; removed committed `__pycache__`/`.pyc` files from the repository

### Changed
- The panel is now always put to sleep after displaying (also on error), preventing high-voltage damage
- `refresh=True` now performs a full panel clear before drawing (previously a no-op); disable for faster updates
- README: documented required packages (`Pillow`, `spidev`, `gpiozero`) and install/demo instructions

### Fixed
- `epdconfig.py`: missing `raise` when `DEV_Config.so` could not be found
- `epdconfig.py`: `digital_read()` read from pin numbers instead of GPIO objects
- Image files are now closed after loading
- Removed unused `numpy` dependency

## [0.5.0] - 2026-01-21
### Added
- Initial release
- `display_image()` API
- Support for fit / fill / stretch scaling modes
- Automatic color detection for supported EPDs
- Added `pyproject.toml`