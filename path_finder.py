import sys
import os

def resource_path(relative_path):
    # Adjusts paths for PyInstaller's temporary directory
    base_path = getattr(sys, '_MEIPASS', os.path.abspath("."))
    return os.path.join(base_path, relative_path)
