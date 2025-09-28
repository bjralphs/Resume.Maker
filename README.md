# Resume Maker (Tkinter + Jinja2 + WeasyPrint)

Simplify the process of creating a professionally formatted resume. This desktop app lets you enter your information in a clean Tkinter UI, preview the generated HTML, and export a pixel‑perfect PDF using WeasyPrint.

> **Why this project?** Content first, styling second. Keep all your resume data as structured JSON while rendering to any number of HTML/CSS templates.

---

## ✨ Features

* **Friendly GUI** built with Tkinter, including long‑form scrolling and list editors for Skills, Experience, Education, and Projects.
* **Live HTML preview** in your default browser.
* **One‑click export** to HTML or **print‑ready PDF** via WeasyPrint.
* **Import/Export JSON** to version your resume content.
* **Template‑driven** rendering powered by Jinja2 (swap CSS without touching your data).
* **Windows‑friendly** PDF bootstrap (adds common GTK/WeasyPrint DLL locations automatically).

---

## 📦 Requirements

* Python 3.9+
* `Jinja2>=3.1`
* `WeasyPrint>=61`

Install dependencies:

```bash
pip install -r requirements.txt
```

> **Windows note:** WeasyPrint requires GTK/Cairo libraries. This app tries to help by adding common DLL locations to the search path at runtime. If you still see DLL errors, install a GTK3 runtime and ensure its `bin` folder is on `PATH`.

---

## 🚀 Quickstart

```bash
# 1) Install deps
pip install -r requirements.txt

# 2) Run the app
python main.py
```

**Basic flow:**

1. Fill out personal info, summary, skills, experience, education, and (optional) projects.
2. Click **Preview (HTML)** to open a generated HTML resume in your browser.
3. Click **Export HTML…** or **Export PDF…** to save your resume.
4. Use **Save JSON…**/**Load JSON…** to backup/restore your content.

---

## 🧠 How it works

```
Tkinter UI  →  Collects structured data
Jinja2      →  Renders `templates/resume.html.j2` using your data
WeasyPrint  →  Converts rendered HTML → PDF
```

* `rendering.py` loads the Jinja2 environment and renders your template to a string/file.
* `pdf_utils.py` calls WeasyPrint to write a PDF from the rendered HTML.
* `app_controller.py` wires the buttons to actions (load/save, preview, export).

---

## 🎨 Templates

Place your HTML template at:

```
templates/resume.html.j2
```

A minimal starting point:

```html
<!doctype html>
<html>
<head>
  <meta charset="utf-8">
  <title>{{ personal.name }} – Resume</title>
  <style>
    @page { size: A4; margin: 10mm; }
    body { font-family: system-ui, -apple-system, Segoe UI, Roboto, Arial, sans-serif; }
    h2 { margin: 0.75rem 0 0.25rem; }
    .section { margin-top: 1rem; }
    .skills { display: grid; grid-template-columns: repeat(3, 1fr); gap: 6pt 10pt; }
  </style>
</head>
<body>
  <h1>{{ personal.name }}</h1>
  <div>{{ personal.location }} | {{ personal.phone }} | {{ personal.email }} | {{ personal.linkedin }}</div>

  <div class="section">
    <h2>OBJECTIVE</h2>
    <p>{{ summary }}</p>
  </div>

  <div class="section">
    <h2>SKILLS</h2>
    <div class="skills">
      {% for s in skills %}<span>• {{ s }}</span>{% endfor %}
    </div>
  </div>

  <div class="section">
    <h2>PROFESSIONAL EXPERIENCE</h2>
    {% for e in experience %}
      <div>
        <strong>{{ e.role }}</strong> — {{ e.company }} <em>({{ e.start }} – {{ e.end }})</em>
        <div>{{ e.location }}</div>
        {% if e.blurb %}<div>{{ e.blurb }}</div>{% endif %}
        {% if e.highlights %}
          <ul>
            {% for h in e.highlights %}<li>{{ h }}</li>{% endfor %}
          </ul>
        {% endif %}
      </div>
    {% endfor %}
  </div>

  <div class="section">
    <h2>EDUCATION</h2>
    {% for ed in education %}
      <div>
        <strong>{{ ed.degree }}</strong> — {{ ed.school }} <em>({{ ed.start }} – {{ ed.end }})</em>
        <div>{{ ed.location }}</div>
        {% if ed.details %}<div>{{ ed.details }}</div>{% endif %}
      </div>
    {% endfor %}
  </div>

  {% if projects %}
  <div class="section">
    <h2>RECENT PROJECTS</h2>
    {% for p in projects %}
      <div>
        <strong>{{ p.name }}</strong> {% if p.link %}— <a href="{{ p.link }}">{{ p.link }}</a>{% endif %}
        <div>{{ p.description }}</div>
        {% if p.bullets %}
          <ul>
            {% for b in p.bullets %}<li>{{ b }}</li>{% endfor %}
          </ul>
        {% endif %}
      </div>
    {% endfor %}
  </div>
  {% endif %}
</body>
</html>
```

> You can inspect `resume_preview.html` for ideas on spacing and CSS rules.

---

## 🧾 JSON shape

This is roughly what gets saved/loaded (see `_collect()` in the controller):

```jsonc
{
  "personal": {
    "name": "Jane Doe",
    "email": "jane@example.com",
    "phone": "(555) 123‑4567",
    "location": "Denver, CO",
    "linkedin": "https://linkedin.com/in/janedoe"
  },
  "summary": "One to three sentences about your value.",
  "skills": ["Python", "SQL", "Git"],
  "experience": [
    {
      "role": "Software Engineer",
      "company": "Acme Corp",
      "start": "Jan 2023",
      "end": "Present",
      "location": "Remote",
      "blurb": "Optional one‑liner.",
      "highlights": ["Impactful bullet 1", "Impactful bullet 2"]
    }
  ],
  "education": [
    {
      "degree": "B.S. in Computer Science",
      "school": "State University",
      "start": "2019",
      "end": "2023",
      "location": "City, ST",
      "details": "Optional details"
    }
  ],
  "projects": [
    {
      "name": "Cool Project",
      "link": "https://github.com/jane/cool-project",
      "description": "Short, one‑line description.",
      "bullets": ["What it does", "How it helped"]
    }
  ]
}
```

---

## 🗂️ Project structure

```
.
├─ main.py                     # Entry point (calls resume_gui.app.run)
├─ resume_preview.html         # Example output for reference
├─ requirements.txt
├─ resume_gui/
│  ├─ app.py                   # Tk root/window & bootstrapping
│  ├─ controllers/
│  │  └─ app_controller.py     # Button handlers, data flow, file actions
│  ├─ services/
│  │  ├─ paths.py              # Template paths & app title
│  │  ├─ rendering.py          # Jinja2 rendering
│  │  └─ pdf_utils.py          # WeasyPrint PDF export (+ DLL bootstrap)
│  ├─ widgets/
│  │  └─ scrollable.py         # Reusable scrollable Tkinter frame
│  ├─ views/
│  │  └─ main_view.py          # The form UI (fields, listboxes, buttons)
│  └─ dialogs.py               # Data entry dialogs (skills, exp, edu, projects)
└─ templates/
   └─ resume.html.j2           # Your HTML/CSS template (create this)
```

---

## 🧪 Development notes

* The Skills, Experience, Education, and Projects listboxes now include scrolling and larger default heights to better handle long lists.
* The form uses a scrollable content area so fields remain usable on small screens.
* `APP_TITLE` is defined in `services/paths.py` (currently **"Resume Maker"**).

### Extending

* Add new fields to the UI (`views/main_view.py`) and plumb them through `_collect()` in `controllers/app_controller.py`.
* Reference the new fields in your Jinja template.

---

## 🛠️ Troubleshooting

* **WeasyPrint/GTK errors on Windows**: Install a GTK3 runtime and ensure its `bin` folder is in your `PATH`. The app also tries a set of common directories automatically.
* **PDF fonts/look different**: PDF output depends on system fonts. Declare web‑safe fonts in your CSS or bundle @font‑face.
* **Page breaks**: Use CSS like `h2 { page-break-after: avoid; }` and `@page { size: A4; margin: 10mm; }` in your template.

---

## 🙌 Acknowledgments

* Built with Tkinter, Jinja2, and WeasyPrint.

---

## 📣 Contributing

PRs welcome! If you spot a bug or want a new field/component, open an issue describing your use case and expected behavior.
