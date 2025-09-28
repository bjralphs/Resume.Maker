# resume_gui/dialogs.py
from tkinter import Toplevel, StringVar, Text, Label, Entry, Button, END, Frame

def _simple_input_dialog(root, title, label, value=""):
    win = Toplevel(root); win.title(title); win.grab_set()
    v = StringVar(value=value)
    Label(win, text=label).pack(anchor="w"); Entry(win, textvariable=v).pack(fill="x")
    out = {}
    def ok(): out["value"] = v.get().strip(); win.destroy()
    def cancel(): out.clear(); win.destroy()
    b = Frame(win); b.pack(pady=8)
    Button(b, text="OK", command=ok).pack(side="left", padx=4)
    Button(b, text="Cancel", command=cancel).pack(side="left", padx=4)
    win.wait_window()
    return out.get("value")

def skill_dialog(root, value=""):
    return _simple_input_dialog(root, "Skill", "Skill", value)

def experience_dialog(root, e=None):
    win = Toplevel(root); win.title("Experience"); 
    win.geometry("600x400")
    win.resizable(True, True)
    win.grab_set()
    fields = {k: StringVar(value=(e or {}).get(k,"")) for k in ["role","company","start","end","location","blurb"]}
    for label, key in [("Role","role"), ("Company","company"), ("Start (e.g., Jan 2022)","start"),
                       ("End (e.g., Jan 2023, Present)","end"), ("Location — (Remote/Hybrid/In-Person)","location"), ("One-line blurb (optional)","blurb")]:
        Label(win, text=label).pack(anchor="w"); Entry(win, textvariable=fields[key]).pack(fill="x")

    Label(win, text="Highlights (one per line)").pack(anchor="w")
    txt = Text(win, height=8); txt.pack(fill="both")
    for h in (e or {}).get("highlights", []): txt.insert(END, h + "\n")

    out = {}
    def ok():
        highlights = [l.strip() for l in txt.get("1.0", END).splitlines() if l.strip()]
        out.update({k: v.get().strip() for k,v in fields.items()}); out["highlights"] = highlights; win.destroy()
    def cancel(): out.clear(); win.destroy()
    b = Frame(win); b.pack(pady=8)
    Button(b, text="OK", command=ok).pack(side="left", padx=4)
    Button(b, text="Cancel", command=cancel).pack(side="left", padx=4)
    win.wait_window()
    return out if out else None

def education_dialog(root, ed=None):
    win = Toplevel(root); win.title("Education"); 
    win.geometry("600x400")
    win.resizable(True, True)
    win.grab_set()
    fields = {k: StringVar(value=(ed or {}).get(k,"")) for k in ["degree","school","start","end","location","details"]}
    for label, key in [("Degree","degree"), ("School","school"), ("Start (e.g., 2019)","start"),
                       ("End (e.g., 2023 or Present)","end"), ("Location","location"), ("Details","details")]:
        Label(win, text=label).pack(anchor="w"); Entry(win, textvariable=fields[key]).pack(fill="x")
    out = {}
    def ok(): out.update({k: v.get().strip() for k,v in fields.items()}); win.destroy()
    def cancel(): out.clear(); win.destroy()
    b = Frame(win); b.pack(pady=8)
    Button(b, text="OK", command=ok).pack(side="left", padx=4)
    Button(b, text="Cancel", command=cancel).pack(side="left", padx=4)
    win.wait_window()
    return out if out else None

def project_dialog(root, p=None):
    win = Toplevel(root); win.title("Project"); 
    win.geometry("600x400")
    win.resizable(True, True)
    win.grab_set()
    fields = {k: StringVar(value=(p or {}).get(k,"")) for k in ["name","link","description"]}
    for label, key in [("Name","name"), ("Link","link"), ("Description (one line)","description")]:
        Label(win, text=label).pack(anchor="w"); Entry(win, textvariable=fields[key]).pack(fill="x")
    Label(win, text="Bullets (one per line)").pack(anchor="w")
    txt = Text(win, height=6); txt.pack(fill="both")
    for b in (p or {}).get("bullets", []): txt.insert(END, b + "\n")
    out = {}
    def ok():
        bullets = [l.strip() for l in txt.get("1.0", END).splitlines() if l.strip()]
        out.update({k: v.get().strip() for k,v in fields.items()}); out["bullets"] = bullets; win.destroy()
    def cancel(): out.clear(); win.destroy()
    b = Frame(win); b.pack(pady=8)
    Button(b, text="OK", command=ok).pack(side="left", padx=4)
    Button(b, text="Cancel", command=cancel).pack(side="left", padx=4)
    win.wait_window()
    return out if out else None
