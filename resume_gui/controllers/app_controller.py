# resume_gui/controllers/app_controller.py
import os, webbrowser
from tkinter import END, messagebox, filedialog
from ..services.rendering import render_resume_html_file, render_resume_html_string
from ..services.pdf_utils import export_pdf_from_html_string
from ..services.storage import save_json, load_json
from ..dialogs import skill_dialog, experience_dialog, education_dialog, project_dialog

class AppController:
    def __init__(self, root, view):
        self.root = root
        self.view = view

        # in-memory data
        self.skills = []
        self.experience = []
        self.education = []
        self.projects = []

    # Bind view buttons to handlers
    def bind(self):
        v = self.view
        v.btn_skill_add.configure(command=self.add_skill)
        v.btn_skill_edit.configure(command=self.edit_skill)
        v.btn_skill_del.configure(command=self.remove_skill)

        v.btn_exp_add.configure(command=self.add_experience)
        v.btn_exp_edit.configure(command=self.edit_experience)
        v.btn_exp_del.configure(command=self.remove_experience)

        v.btn_edu_add.configure(command=self.add_education)
        v.btn_edu_edit.configure(command=self.edit_education)
        v.btn_edu_del.configure(command=self.remove_education)

        v.btn_prj_add.configure(command=self.add_project)
        v.btn_prj_edit.configure(command=self.edit_project)
        v.btn_prj_del.configure(command=self.remove_project)

        v.btn_load.configure(command=self.on_load)
        v.btn_save.configure(command=self.on_save)
        v.btn_prev.configure(command=self.on_preview)
        v.btn_export.configure(command=self.on_export_html)
        v.btn_pdf.configure(command=self.on_export_pdf)

    # ---------- Skills ----------
    def add_skill(self):
        s = skill_dialog(self.root, "")
        if s:
            self.skills.append(s)
            self.view.lb_sk.insert(END, s)

    def edit_skill(self):
        sel = self.view.lb_sk.curselection()
        if not sel: return
        i = sel[0]
        s = skill_dialog(self.root, self.skills[i])
        if s:
            self.skills[i] = s
            self.view.lb_sk.delete(i); self.view.lb_sk.insert(i, s)

    def remove_skill(self):
        sel = self.view.lb_sk.curselection()
        if not sel: return
        i = sel[0]
        del self.skills[i]; self.view.lb_sk.delete(i)

    # ---------- Experience ----------
    def _exp_summary(self, e):
        left  = " — ".join([x for x in [e.get("role",""), e.get("company","")] if x])
        right = " ".join([e.get("start",""), "–", e.get("end","")]).strip(" –")
        tail  = " · ".join([p for p in [right, e.get("location","")] if p])
        return " | ".join([p for p in [left, tail] if p])

    def add_experience(self):
        item = experience_dialog(self.root, None)
        if item:
            self.experience.append(item)
            self.view.lb_ex.insert(END, self._exp_summary(item))

    def edit_experience(self):
        sel = self.view.lb_ex.curselection()
        if not sel: return
        i = sel[0]
        updated = experience_dialog(self.root, self.experience[i])
        if updated:
            self.experience[i] = updated
            self.view.lb_ex.delete(i); self.view.lb_ex.insert(i, self._exp_summary(updated))

    def remove_experience(self):
        sel = self.view.lb_ex.curselection()
        if not sel: return
        i = sel[0]
        del self.experience[i]; self.view.lb_ex.delete(i)

    # ---------- Education ----------
    def _edu_summary(self, ed):
        parts = [ed.get("degree",""), ed.get("school","")]
        when  = " ".join([ed.get("start",""), "–", ed.get("end","")]).strip(" –")
        loc   = ed.get("location","")
        tail  = " · ".join([p for p in [when, loc] if p])
        return " — ".join([p for p in [" | ".join([x for x in parts if x]), tail] if p])

    def add_education(self):
        item = education_dialog(self.root, None)
        if item:
            self.education.append(item)
            self.view.lb_ed.insert(END, self._edu_summary(item))

    def edit_education(self):
        sel = self.view.lb_ed.curselection()
        if not sel: return
        i = sel[0]
        updated = education_dialog(self.root, self.education[i])
        if updated:
            self.education[i] = updated
            self.view.lb_ed.delete(i); self.view.lb_ed.insert(i, self._edu_summary(updated))

    def remove_education(self):
        sel = self.view.lb_ed.curselection()
        if not sel: return
        i = sel[0]
        del self.education[i]; self.view.lb_ed.delete(i)

    # ---------- Projects ----------
    def _prj_summary(self, p):
        return " — ".join([x for x in [p.get("name",""), p.get("link","")] if x])

    def add_project(self):
        item = project_dialog(self.root, None)
        if item:
            self.projects.append(item)
            self.view.lb_pr.insert(END, self._prj_summary(item))

    def edit_project(self):
        sel = self.view.lb_pr.curselection()
        if not sel: return
        i = sel[0]
        updated = project_dialog(self.root, self.projects[i])
        if updated:
            self.projects[i] = updated
            self.view.lb_pr.delete(i); self.view.lb_pr.insert(i, self._prj_summary(updated))

    def remove_project(self):
        sel = self.view.lb_pr.curselection()
        if not sel: return
        i = sel[0]
        del self.projects[i]; self.view.lb_pr.delete(i)

    # ---------- Aggregation ----------
    def _collect(self):
        return {
            "personal": self.view.get_personal(),
            "summary": self.view.get_summary(),
            "skills_style": "tags",  # or self.view.skills_style.get()
            "skills": list(self.skills),
            "experience": list(self.experience),
            "education": list(self.education),
            "projects": list(self.projects),
        }

    # ---------- File actions ----------
    def on_load(self):
        path = filedialog.askopenfilename(filetypes=[("JSON", "*.json")])
        if not path: return
        try:
            data = load_json(path)
            self.view.set_personal(data.get("personal", {}))
            self.view.set_summary(data.get("summary", ""))
            # rebuild lists
            self.skills = list(data.get("skills", []))
            self.experience = list(data.get("experience", []))
            self.education  = list(data.get("education", []))
            self.projects   = list(data.get("projects", []))
            # repaint listboxes
            self.view.lb_sk.delete(0, "end");  [self.view.lb_sk.insert("end", s) for s in self.skills]
            self.view.lb_ex.delete(0, "end");  [self.view.lb_ex.insert("end", self._exp_summary(e)) for e in self.experience]
            self.view.lb_ed.delete(0, "end");  [self.view.lb_ed.insert("end", self._edu_summary(ed)) for ed in self.education]
            self.view.lb_pr.delete(0, "end");  [self.view.lb_pr.insert("end", self._prj_summary(p)) for p in self.projects]
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def on_save(self):
        data = self._collect()
        path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON", "*.json")])
        if not path: return
        try:
            save_json(data, path)
            messagebox.showinfo("Saved", "Saved form data to JSON.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def on_preview(self):
        data = self._collect()
        out = os.path.abspath("resume_preview.html")
        try:
            render_resume_html_file(data, out)
            webbrowser.open_new_tab(f"file://{out}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def on_export_html(self):
        data = self._collect()
        path = filedialog.asksaveasfilename(defaultextension=".html", filetypes=[("HTML", "*.html")])
        if not path: return
        try:
            render_resume_html_file(data, path)
            messagebox.showinfo("Exported", "Exported resume HTML.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def on_export_pdf(self):
        data = self._collect()
        path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF", "*.pdf")])
        if not path: return
        try:
            html = render_resume_html_string(data)
            export_pdf_from_html_string(html, path)
            messagebox.showinfo("Exported", "Exported resume PDF.")
        except Exception as e:
            messagebox.showerror("Error", str(e))
