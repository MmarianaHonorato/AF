import tkinter as tk
from tkinter import font as tkfont


class AlongamentoPage(tk.Frame):
    def __init__(self, parent, app=None):
        super().__init__(parent, bg="#d9d9d9")
        self.app = app

        self.f_titulo    = tkfont.Font(family="Helvetica", size=36, weight="bold")
        self.f_descricao = tkfont.Font(family="Helvetica", size=24)
        self.f_relogio   = tkfont.Font(family="Helvetica", size=80, weight="bold")

        self.var_nome      = tk.StringVar(value="Preparando...")
        self.var_descricao = tk.StringVar(value="...")
        self.var_tempo     = tk.StringVar(value="00:00")

        self.tempo_restante = 0
        self.timer_id = None

        self._build()

        if self.app and hasattr(self.app, 'config_tema_escuro'):
            self.aplicar_tema(self.app.config_tema_escuro)

    def _build(self):
        self.caixa = tk.Frame(self, bg="white", padx=50, pady=50)
        self.caixa.pack(expand=True)

        self.lbl_subtitulo = tk.Label(
            self.caixa, text="✨ Hora de Alongar! ✨",
            font=("Helvetica", 20, "bold"), fg="#a7f3d0", bg="white"
        )
        self.lbl_subtitulo.pack(pady=(0, 10))

        self.lbl_nome = tk.Label(
            self.caixa, textvariable=self.var_nome,
            font=self.f_titulo, fg="#1A1A1A", bg="white"
        )
        self.lbl_nome.pack(pady=10)

        self.lbl_descricao = tk.Label(
            self.caixa, textvariable=self.var_descricao,
            font=self.f_descricao, fg="#444444", bg="white"
        )
        self.lbl_descricao.pack(pady=20)

        self.lbl_relogio = tk.Label(
            self.caixa, textvariable=self.var_tempo,
            font=self.f_relogio, fg="#1A1A1A", bg="white"
        )
        self.lbl_relogio.pack(pady=40)

        self.btn_pular = tk.Button(
            self.caixa, text="Pular Alongamento",
            bg="#e5e7eb", font=("Helvetica", 16),
            relief="flat", padx=20, pady=10,
            command=self.finalizar_alongamento
        )
        self.btn_pular.pack(pady=10)

    def iniciar_alongamento(self, alongamento):
        self.var_nome.set(alongamento.nome)
        self.var_descricao.set(alongamento.descricao)
        self.tempo_restante = alongamento.duracao
        self.atualizar_interface()
        self.contar_tempo()

    def contar_tempo(self):
        if self.tempo_restante > 0:
            self.tempo_restante -= 1
            self.atualizar_interface()
            self.timer_id = self.after(1000, self.contar_tempo)
        else:
            self.finalizar_alongamento()

    def atualizar_interface(self):
        m, s = divmod(self.tempo_restante, 60)
        self.var_tempo.set(f"{m:02d}:{s:02d}")

    def finalizar_alongamento(self):
        if self.timer_id:
            self.after_cancel(self.timer_id)
            self.timer_id = None
        self.app.sessao_controller.finalizar_pausa_alongamento()

    # ── TEMA ──────────────────────────────────────────────────────────────
    def aplicar_tema(self, escuro: bool):
        cor_fundo  = "#1E1E1E" if escuro else "#d9d9d9"
        cor_cartao = "#2D2D2D" if escuro else "white"
        cor_texto  = "#FFFFFF" if escuro else "#1A1A1A"
        cor_sub    = "#CCCCCC" if escuro else "#444444"
        cor_botao  = "#3A3A3A" if escuro else "#e5e7eb"

        self.configure(bg=cor_fundo)
        self.caixa.configure(bg=cor_cartao)
        self.lbl_subtitulo.configure(bg=cor_cartao)
        self.lbl_nome.configure(bg=cor_cartao, fg=cor_texto)
        self.lbl_descricao.configure(bg=cor_cartao, fg=cor_sub)
        self.lbl_relogio.configure(bg=cor_cartao, fg=cor_texto)
        self.btn_pular.configure(bg=cor_botao, fg=cor_texto,
                                 activebackground=cor_botao, activeforeground=cor_texto)
