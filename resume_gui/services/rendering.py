# resume_gui/services/rendering.py
from jinja2 import Environment, FileSystemLoader, select_autoescape
from .paths import TEMPLATE_DIR, TEMPLATE_NAME

def render_resume_html_string(data: dict) -> str:
    env = Environment(
        loader=FileSystemLoader(TEMPLATE_DIR),
        autoescape=select_autoescape(["html", "xml"])
    )
    return env.get_template(TEMPLATE_NAME).render(**data)

def render_resume_html_file(data: dict, out_html_path: str) -> str:
    html = render_resume_html_string(data)
    with open(out_html_path, "w", encoding="utf-8") as f:
        f.write(html)
    return out_html_path
