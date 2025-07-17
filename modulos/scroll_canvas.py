import tkinter as tk

class ScrollCanvas(tk.Canvas):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, width=10, bg="#1e1e1e", highlightthickness=0, bd=0, **kwargs)
        self.thumb = self.create_rectangle(2, 0, 8, 40, fill="#3a3a3a", outline="#3a3a3a")
        self.scroll_target = None

        self.bind("<Button-1>", self.start_scroll)
        self.bind("<B1-Motion>", self.do_scroll)

    def connect(self, widget):
        self.scroll_target = widget
        widget.config(yscrollcommand=self.update_thumb)
        widget.bind("<MouseWheel>", self.scroll_mouse)

    def update_thumb(self, first, last):
        top = float(first)
        height = float(last) - top
        canvas_height = self.winfo_height()
        thumb_top = int(top * canvas_height)
        thumb_bottom = int((top + height) * canvas_height)
        self.coords(self.thumb, 2, thumb_top, 8, thumb_bottom)

    def scroll_mouse(self, event):
        if self.scroll_target:
            direction = -1 if event.delta > 0 else 1
            self.scroll_target.yview_scroll(direction, "units")

    def start_scroll(self, event):
        self.scan_mark(event.x, event.y)

    def do_scroll(self, event):
        thumb_coords = self.coords(self.thumb)
        delta_y = event.y - thumb_coords[1]
        fraction = delta_y / self.winfo_height()
        self.scroll_target.yview_moveto(fraction)