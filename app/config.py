# app/config.py
from pathlib import Path

# Base directory of the application
BASE_DIR = Path(__file__).resolve().parent.parent

# Resource paths
RESOURCES_DIR = BASE_DIR / "resources"
STYLESHEET_PATH = RESOURCES_DIR / "styles.qss"
IMAGES_DIR = RESOURCES_DIR / "images"

# Icon paths
LOGO_ICON = str(IMAGES_DIR / "logo.png")
LIGHT_THEME_ICON = str(IMAGES_DIR / "light.png")
DARK_THEME_ICON = str(IMAGES_DIR / "dark.png")
REFRESH_LIGHT_ICON = str(IMAGES_DIR / "refresh_light.png")
REFRESH_DARK_ICON = str(IMAGES_DIR / "refresh_dark.png")

# API Configuration
API_BASE_URL = "https://api.coingecko.com/api/v3"
API_TIMEOUT = 15