import tkinter as tk
from pathlib import Path


class PopUp(tk.Toplevel):
    def __init__(self, parent, controller, alongamento):
        super().__init__(parent)
        self.controller  = controller
        self.alongamento = alongamento
        self._parent     = parent   # guarda para herdar o tema

        self.tempo_restante = alongamento.duracao
        self.timer_id = None

        self.geometry("380x420")
        self.configure(bg="#A3E4A3")
        self.overrideredirect(True)

        self._x_mouse = 0
        self._y_mouse = 0
        self.assets_dir = Path(__file__).resolve().parent.parent / "assets"

        self.var_nome      = tk.StringVar(value=alongamento.nome)
        self.var_descricao = tk.StringVar(value=alongamento.descricao)
        m, s = divmod(self.tempo_restante, 60)
        self.var_duracao = tk.StringVar(value=f"{m}:{s:02d}")

        self._build_barra_superior()
        self._build_cartao_principal()
        self._centralizar()

        # Aplica o tema herdado do app
        if hasattr(self._parent, 'config_tema_escuro'):
            self._aplicar_tema_popup(self._parent.config_tema_escuro)

    def _build_barra_superior(self):
        topo = tk.Frame(self, bg="#A3E4A3")
        topo.pack(fill="x", padx=10, pady=5)
        self.topo = topo

        topo.bind("<Button-1>", self._iniciar_movimento)
        topo.bind("<B1-Motion>", self._mover_janela)

        try:
            caminho_logo = self.assets_dir / "logo.png"
            self.logo_photo = tk.PhotoImage(file=caminho_logo).subsample(4, 4)
            lbl_logo = tk.Label(topo, image=self.logo_photo, bg="#A3E4A3")
            lbl_logo.pack(side="left")
            lbl_logo.bind("<Button-1>", self._iniciar_movimento)
            lbl_logo.bind("<B1-Motion>", self._mover_janela)
        except Exception:
            pass

        self.lbl_app_nome = tk.Label(topo, text="AlongFit", bg="#A3E4A3",
                                     font=("Helvetica", 11, "bold"))
        self.lbl_app_nome.pack(side="left", padx=5)
        self.lbl_app_nome.bind("<Button-1>", self._iniciar_movimento)
        self.lbl_app_nome.bind("<B1-Motion>", self._mover_janela)

        tk.Button(
            topo, text="X", bg="#A3E4A3", fg="black",
            font=("Helvetica", 14, "bold"), relief="flat",
            cursor="hand2", activebackground="#A3E4A3",
            command=self.fechar_pop_up
        ).pack(side="right")

    def _build_cartao_principal(self):
        self.cartao = tk.Frame(self, bg="white")
        self.cartao.pack(fill="both", expand=True, padx=8, pady=(0, 8))

        self.lbl_titulo_along = tk.Label(
            self.cartao, textvariable=self.var_nome,
            bg="white", fg="black", font=("Helvetica", 18, "bold"),
            wraplength=320, justify="center"
        )
        self.lbl_titulo_along.pack(pady=(30, 15))

        self.lbl_desc_along = tk.Label(
            self.cartao, textvariable=self.var_descricao,
            bg="white", fg="black", font=("Helvetica", 16),
            wraplength=320, justify="center"
        )
        self.lbl_desc_along.pack(pady=(0, 30))

        self.lbl_duracao = tk.Label(
            self.cartao, textvariable=self.var_duracao,
            bg="white", fg="black", font=("Helvetica", 28)
        )
        self.lbl_duracao.pack(pady=(0, 30))

        self.btn_iniciar = tk.Button(
            self.cartao, text="Iniciar", bg="#A3E4A3", fg="black",
            font=("Helvetica", 14, "bold"), relief="solid", bd=1,
            padx=30, pady=5, cursor="hand2",
            command=self.iniciar_cronometro_alongamento
        )
        self.btn_iniciar.pack()

    def iniciar_cronometro_alongamento(self):
        self.btn_iniciar.config(state="disabled", text="Alongando...", bg="#e5e7eb")
        self._contar_tempo()

    def _contar_tempo(self):
        if self.tempo_restante > 0:
            self.tempo_restante -= 1
            m, s = divmod(self.tempo_restante, 60)
            self.var_duracao.set(f"{m}:{s:02d}")
            self.controller.ticar_tempo_total_durante_alongamento()
            self.timer_id = self.after(1000, self._contar_tempo)
        else:
            self.fechar_pop_up()

    def fechar_pop_up(self):
        if self.timer_id:
            self.after_cancel(self.timer_id)
        self.controller.retomar_apos_alongamento()
        self.destroy()

    def _centralizar(self):
        self.update_idletasks()
        w, h = self.winfo_width(), self.winfo_height()
        x = (self.winfo_screenwidth()  // 2) - (w // 2)
        y = (self.winfo_screenheight() // 2) - (h // 2)
        self.geometry(f'{w}x{h}+{x}+{y}')

    def _iniciar_movimento(self, event):
        self._x_mouse = event.x
        self._y_mouse = event.y

    def _mover_janela(self, event):
        novo_x = self.winfo_x() + (event.x - self._x_mouse)
        novo_y = self.winfo_y() + (event.y - self._y_mouse)
        self.geometry(f"+{novo_x}+{novo_y}")

    # ── TEMA ──────────────────────────────────────────────────────────────
    def _aplicar_tema_popup(self, escuro: bool):
        # O cabeçalho verde é mantido — só o cartão interno muda
        cor_cartao = "#2D2D2D" if escuro else "white"
        cor_texto  = "#FFFFFF" if escuro else "black"

        self.cartao.configure(bg=cor_cartao)
        self.lbl_titulo_along.configure(bg=cor_cartao, fg=cor_texto)
        self.lbl_desc_along.configure(bg=cor_cartao, fg=cor_texto)
        self.lbl_duracao.configure(bg=cor_cartao, fg=cor_texto)
