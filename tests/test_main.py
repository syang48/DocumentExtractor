import pytest
import subprocess
import sys
import os

# Add the current directory to the path so it can find main.py
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_read_main():
    from main import app  # Now it will find your main.py
    assert app is not None

def test_libreoffice_installed():
    result = subprocess.run(["soffice", "--version"], capture_output=True, text=True)
    assert result.returncode == 0
    assert "LibreOffice" in result.stdout
