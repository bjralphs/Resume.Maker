# resume_gui/app.py
from tkinter import Tk
from .controllers.app_controller import AppController
from .views.main_view import MainView
from .services.paths import APP_TITLE

def run():
    root = Tk()
    root.title(APP_TITLE)
    root.geometry("900x720")      # set size here
    root.minsize(760, 520)

    view = MainView(root)         # build the UI
    controller = AppController(root, view)  # wire handlers
    controller.bind()             # connect buttons -> controller methods

    root.mainloop()
