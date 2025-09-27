# resume_gui/services/paths.py
from pathlib import Path

APP_TITLE = "Resume Maker"
PROJECT_ROOT = Path(__file__).resolve().parents[2]   # your-project/
TEMPLATE_DIR = str(PROJECT_ROOT / "templates")
TEMPLATE_NAME = "resume.html.j2"
