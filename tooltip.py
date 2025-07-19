import tkinter as tk

class Tooltip:
    def __init__(self, widget, text, delay=500):
        self.widget = widget
        self.text = text
        self.tip_window = None
        self.delay = delay
        self.after_id = None

        widget.bind("<Enter>", self.schedule_tooltip)
        widget.bind("<Leave>", self.unschedule_tooltip)

    def schedule_tooltip(self, event=None):
        self.unschedule_tooltip()
        self.after_id = self.widget.after(self.delay, self.show_tooltip)

    def unschedule_tooltip(self, event=None):
        if self.after_id:
            self.widget.after_cancel(self.after_id)
            self.after_id = None
        self.hide_tooltip()

    def show_tooltip(self):
        if self.tip_window or not self.text:
            return
        x = self.widget.winfo_rootx() + 48
        y = self.widget.winfo_rooty() + 32

        self.tip_window = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry(f"+{x}+{y}")
        tw.attributes("-topmost", True)

        label = tk.Label(
            tw,
            text=self.text,
            justify="left",
            background="#ffffe0",
            foreground="#333333",
            relief="solid",
            borderwidth=1,
            font=("Segoe UI", 10, "normal")
        )
        label.pack(ipadx=8, ipady=4)

    def hide_tooltip(self):
        if self.tip_window:
            self.tip_window.destroy()
            self.tip_window = None