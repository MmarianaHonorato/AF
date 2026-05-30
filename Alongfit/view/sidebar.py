import tkinter as tk
from pathlib import Path
from tkinter import font as tkfont

SIDEBAR_BG = "#FFFFFF"
CARD_BG    = "#FFFFFF"
TEXT_DARK  = "#1A1A1A"
BTN_HOVER  = "#C8C8C8"

MENU_ITEMS = [
    ("home",   "homeLogo.png"),
    ("stats",  "status.png"),
    ("timer",  "timer.png"),
    ("config", "config.png"),
]
ACTIVE_PAGE = "home"


class Sidebar(tk.Frame):
    def __init__(self, parent, on_select=None, active_page=ACTIVE_PAGE, **kwargs):
        super().__init__(parent, bg=SIDEBAR_BG, width=120, **kwargs)
        self.pack_propagate(False)

        self.on_select   = on_select
        self.active_page = active_page
        self.buttons     = {}
        self.menu_icons  = {}
        self.assets_dir  = Path(__file__).resolve().parent.parent / "assets"

        self.f_logo = tkfont.Font(family="Helvetica", size=14, weight="bold")
        self.f_item = tkfont.Font(family="Helvetica", size=11)

        self._build()

    def _build(self):
        logo_frame = tk.Frame(self, bg=SIDEBAR_BG)
        logo_frame.pack(pady=(20, 16), padx=10, anchor="w")
        self.logo_frame = logo_frame

        logo_path = self.assets_dir / "logo.png"
        self.logo_photo = tk.PhotoImage(file=logo_path).subsample(2, 2)

        self.lbl_logo_img = tk.Label(logo_frame, image=self.logo_photo, bg=SIDEBAR_BG)
        self.lbl_logo_img.pack(side="left")
        self.lbl_logo_txt = tk.Label(logo_frame, text="AlongFit", bg=SIDEBAR_BG,
                                     font=self.f_logo, fg=TEXT_DARK)
        self.lbl_logo_txt.pack(side="left", padx=4)

        for page_name, image_name in MENU_ITEMS:
            self._menu_button(page_name, image_name)

    def _menu_button(self, page_name, image_name):
        active    = page_name == self.active_page
        bg_normal = CARD_BG if active else SIDEBAR_BG

        container = tk.Frame(self, bg=bg_normal, cursor="hand2", padx=10, pady=10)
        container.pack(padx=10, pady=4)

        icon = tk.PhotoImage(file=self.assets_dir / image_name)
        self.menu_icons[page_name] = icon

        icon_label = tk.Label(container, image=icon, bg=bg_normal)
        icon_label.pack()
        self.buttons[page_name] = (container, icon_label)

        def on_enter(e):
            if page_name != self.active_page:
                container.configure(bg=BTN_HOVER)
                icon_label.configure(bg=BTN_HOVER)

        def on_leave(e):
            if page_name != self.active_page:
                container.configure(bg=self._bg_sidebar)
                icon_label.configure(bg=self._bg_sidebar)

        def on_click(e):
            self.select_page(page_name)

        for w in (container, icon_label):
            w.bind("<Enter>", on_enter)
            w.bind("<Leave>", on_leave)
            w.bind("<Button-1>", on_click)

    @property
    def _bg_sidebar(self):
        return self.cget("bg")

    def select_page(self, page_name):
        self.active_page = page_name
        self._refresh_buttons()
        if self.on_select:
            self.on_select(page_name)

    def _refresh_buttons(self):
        bg_sidebar = self._bg_sidebar
        bg_active  = "#3A3A3A" if bg_sidebar == "#2D2D2D" else CARD_BG
        for page_name, (container, icon_label) in self.buttons.items():
            bg = bg_active if page_name == self.active_page else bg_sidebar
            container.configure(bg=bg)
            icon_label.configure(bg=bg)

    # ── TEMA ──────────────────────────────────────────────────────────────
    def aplicar_tema(self, escuro: bool):
        cor_sidebar = "#2D2D2D" if escuro else SIDEBAR_BG
        cor_texto   = "#FFFFFF" if escuro else TEXT_DARK
        cor_ativo   = "#3A3A3A" if escuro else CARD_BG

        self.configure(bg=cor_sidebar)
        self.logo_frame.configure(bg=cor_sidebar)
        self.lbl_logo_img.configure(bg=cor_sidebar)
        self.lbl_logo_txt.configure(bg=cor_sidebar, fg=cor_texto)

        for page_name, (container, icon_label) in self.buttons.items():
            bg = cor_ativo if page_name == self.active_page else cor_sidebar
            container.configure(bg=bg)
            icon_label.configure(bg=bg)
