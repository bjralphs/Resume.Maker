# resume_gui/services/pdf_utils.py
import os
# --- WeasyPrint DLL bootstrap (Windows)
PREFERRED_GTK_BIN = r"C:\Program Files\GTK3-Runtime Win64\bin"
CANDIDATE_DLL_DIRS = [
    PREFERRED_GTK_BIN,
    r"C:\Program Files\GTK3-Runtime\bin",
    r"C:\Program Files (x86)\GTK3-Runtime\bin",
    r"C:\msys64\ucrt64\bin",
    r"C:\msys64\mingw64\bin",
]
def _bootstrap_weasyprint_dlls():
    added = []
    if hasattr(os, "add_dll_directory"):
        for d in CANDIDATE_DLL_DIRS:
            if d and os.path.isdir(d):
                os.add_dll_directory(d); added.append(d)
    else:
        for d in CANDIDATE_DLL_DIRS:
            if d and os.path.isdir(d):
                os.environ["PATH"] = d + os.pathsep + os.environ.get("PATH",""); added.append(d)
    return added
_ADDED_DLL_DIRS = _bootstrap_weasyprint_dlls()

from weasyprint import HTML  # noqa: E402

def export_pdf_from_html_string(html_string: str, out_pdf_path: str) -> str:
    HTML(string=html_string, base_url=os.path.abspath(".")).write_pdf(out_pdf_path)
    return out_pdf_path
