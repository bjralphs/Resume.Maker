# resume_gui/views/main_view.py
import webbrowser
from tkinter import (
    StringVar, Text, Label, Entry, Button, END, Toplevel, Listbox, SINGLE, Frame
)
from . .widgets.scrollable import ScrollableFrame

class MainView:
    def __init__(self, root):
        self.root = root

        # Scrollable area for long form
        container = ScrollableFrame(root)
        container.pack(fill="both", expand=True)
        form = container.scrollable_frame

        # ---- Personal
        Label(form, text="Full Name").pack(anchor="w")
        self.name = StringVar(); Entry(form, textvariable=self.name).pack(fill="x")
        Label(form, text="Email").pack(anchor="w")
        self.email = StringVar(); Entry(form, textvariable=self.email).pack(fill="x")
        Label(form, text="Phone").pack(anchor="w")
        self.phone = StringVar(); Entry(form, textvariable=self.phone).pack(fill="x")
        Label(form, text="Location (City, State)").pack(anchor="w")
        self.location = StringVar(); Entry(form, textvariable=self.location).pack(fill="x")

        Label(form, text="Professional Title").pack(anchor="w")
        self.title = StringVar(); Entry(form, textvariable=self.title).pack(fill="x")
        Label(form, text="LinkedIn URL").pack(anchor="w")
        self.linkedin = StringVar(); Entry(form, textvariable=self.linkedin).pack(fill="x")
        Label(form, text="Website/Portfolio").pack(anchor="w")
        self.website = StringVar(); Entry(form, textvariable=self.website).pack(fill="x")

        Label(form, text="Skills style (tags|grid)").pack(anchor="w")
        self.skills_style = StringVar(value="tags"); Entry(form, textvariable=self.skills_style).pack(fill="x")

        # ---- Summary
        Label(form, text="Summary (1–3 sentences)").pack(anchor="w")
        self.summary = Text(form, height=4); self.summary.pack(fill="both")

        # ---- Skills
        Label(form, text="Skills").pack(anchor="w", pady=(10, 0))
        self.skill_items = []
        self.lb_sk = Listbox(form, height=6, selectmode=SINGLE); self.lb_sk.pack(fill="both")
        row_sk = Frame(form); row_sk.pack(fill="x", pady=4)
        self.btn_skill_add = Button(row_sk, text="Add Skill…")
        self.btn_skill_edit = Button(row_sk, text="Edit…")
        self.btn_skill_del  = Button(row_sk, text="Remove")
        self.btn_skill_add.pack(side="left"); self.btn_skill_edit.pack(side="left", padx=6); self.btn_skill_del.pack(side="left")

        # ---- Experience
        Label(form, text="Professional Experience").pack(anchor="w", pady=(12, 0))
        self.experience_items = []
        self.lb_ex = Listbox(form, height=8, selectmode=SINGLE); self.lb_ex.pack(fill="both")
        row_ex = Frame(form); row_ex.pack(fill="x", pady=4)
        self.btn_exp_add = Button(row_ex, text="Add Experience…")
        self.btn_exp_edit = Button(row_ex, text="Edit…")
        self.btn_exp_del  = Button(row_ex, text="Remove")
        self.btn_exp_add.pack(side="left"); self.btn_exp_edit.pack(side="left", padx=6); self.btn_exp_del.pack(side="left")

        # ---- Education
        Label(form, text="Education").pack(anchor="w", pady=(10, 0))
        self.education_items = []
        self.lb_ed = Listbox(form, height=6, selectmode=SINGLE); self.lb_ed.pack(fill="both")
        row_ed = Frame(form); row_ed.pack(fill="x", pady=4)
        self.btn_edu_add = Button(row_ed, text="Add Education…")
        self.btn_edu_edit = Button(row_ed, text="Edit…")
        self.btn_edu_del  = Button(row_ed, text="Remove")
        self.btn_edu_add.pack(side="left"); self.btn_edu_edit.pack(side="left", padx=6); self.btn_edu_del.pack(side="left")

        # ---- Projects
        Label(form, text="Projects").pack(anchor="w", pady=(12, 0))
        self.project_items = []
        self.lb_pr = Listbox(form, height=6, selectmode=SINGLE); self.lb_pr.pack(fill="both")
        row_pr = Frame(form); row_pr.pack(fill="x", pady=4)
        self.btn_prj_add = Button(row_pr, text="Add Project…")
        self.btn_prj_edit = Button(row_pr, text="Edit…")
        self.btn_prj_del  = Button(row_pr, text="Remove")
        self.btn_prj_add.pack(side="left"); self.btn_prj_edit.pack(side="left", padx=6); self.btn_prj_del.pack(side="left")

        # ---- Footer (fixed)
        footer = Frame(root); footer.pack(fill="x", padx=8, pady=8)
        self.btn_load   = Button(footer, text="Load JSON…");  self.btn_load.pack(side="left")
        self.btn_save   = Button(footer, text="Save JSON…");  self.btn_save.pack(side="left", padx=6)
        self.btn_prev   = Button(footer, text="Preview (HTML)"); self.btn_prev.pack(side="right")
        self.btn_export = Button(footer, text="Export HTML…");   self.btn_export.pack(side="right", padx=6)
        self.btn_pdf    = Button(footer, text="Export PDF…");    self.btn_pdf.pack(side="right")

    # Helpers for controller to access form data
    def get_personal(self):
        return {
            "name": self.name.get().strip(),
            "email": self.email.get().strip(),
            "phone": self.phone.get().strip(),
            "location": self.location.get().strip(),
            "title": self.title.get().strip(),
            "linkedin": self.linkedin.get().strip(),
            "website": self.website.get().strip(),
        }

    def set_personal(self, d):
        self.name.set(d.get("name","")); self.email.set(d.get("email",""))
        self.phone.set(d.get("phone","")); self.location.set(d.get("location",""))
        self.title.set(d.get("title","")); self.linkedin.set(d.get("linkedin",""))
        self.website.set(d.get("website",""))

    def get_summary(self): return self.summary.get("1.0", "end").strip()
    def set_summary(self, text): self.summary.delete("1.0", "end"); self.summary.insert("1.0", text)
