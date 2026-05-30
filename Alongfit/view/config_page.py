import tkinter as tk
from tkinter import ttk


class ConfigPage(tk.Frame):
    def __init__(self, parent, app=None):
        super().__init__(parent, bg="#D9D9D9")
        self.app = app

        if self.app:
            if not hasattr(self.app, 'config_tema_escuro'):
                self.app.config_tema_escuro = False
            if not hasattr(self.app, 'config_sons'):
                self.app.config_sons = True
            if not hasattr(self.app, 'config_hidratacao'):
                self.app.config_hidratacao = False
            if not hasattr(self.app, 'config_frequencia_agua'):
                self.app.config_frequencia_agua = "A cada 1 hora"

        tema_inicial = self.app.config_tema_escuro     if self.app else False
        sons_inicial = self.app.config_sons            if self.app else True
        hidr_inicial = self.app.config_hidratacao      if self.app else False
        freq_inicial = self.app.config_frequencia_agua if self.app else "A cada 1 hora"

        self.var_tema_escuro     = tk.BooleanVar(value=tema_inicial)
        self.var_sons            = tk.BooleanVar(value=sons_inicial)
        self.var_hidratacao      = tk.BooleanVar(value=hidr_inicial)
        self.var_frequencia_agua = tk.StringVar(value=freq_inicial)

        self._build()
        self.aplicar_tema(tema_inicial)
        self._atualizar_estado_hidratacao()

    def _build(self):
        self.contorno = tk.Frame(self, bg="#D9D9D9", width=1300, height=1400)
        self.contorno.pack(anchor="c", expand=True, fill="both")
        self.contorno.pack_propagate(False)

        self.barra_superior = tk.Frame(self.contorno, bg="#D9D9D9")
        self.barra_superior.pack(fill="x", padx=30, pady=20)

        self.lbl_titulo_barra = tk.Label(
            self.barra_superior, text="Aquecimento - Antes de iniciar!",
            bg="#D9D9D9", fg="#1A1A1A", font=("Helvetica", 18)
        )
        self.lbl_titulo_barra.pack(side="left")

        self.btn_x = tk.Button(
            self.barra_superior, text="X", bg="#D9D9D9", fg="#1A1A1A",
            font=("Helvetica", 20, "bold"), relief="flat",
            cursor="hand2", command=self._voltar
        )
        self.btn_x.pack(side="right")

        self.cartao = tk.Frame(self.contorno, bg="#FFFFFF")
        self.cartao.pack(expand=True, fill="both", padx=60, pady=(0, 60))

        self.conteudo_cartao = tk.Frame(self.cartao, bg="#FFFFFF", padx=50, pady=40)
        self.conteudo_cartao.pack(expand=True, fill="both")

        self.lbl_titulo_config = tk.Label(
            self.conteudo_cartao, text="Configurações", bg="#FFFFFF", fg="#000000",
            font=("Helvetica", 32, "bold")
        )
        self.lbl_titulo_config.pack(pady=(0, 50))

        self.form_frame = tk.Frame(self.conteudo_cartao, bg="#FFFFFF")
        self.form_frame.pack(fill="both", expand=True)

        fonte_labels = ("Helvetica", 20)

        # Linha 1 — Tema escuro
        self.linha_tema = tk.Frame(self.form_frame, bg="#FFFFFF")
        self.linha_tema.pack(fill="x", pady=20)
        tk.Label(self.linha_tema, text="Modo Escuro (Tema)",
                 bg="#FFFFFF", font=fonte_labels).pack(side="left")
        self.chk_tema = tk.Checkbutton(
            self.linha_tema, bg="#FFFFFF", variable=self.var_tema_escuro,
            cursor="hand2", command=self._ao_clicar_no_tema
        )
        self.chk_tema.pack(side="right")

        # Linha 2 — Sons (CORRIGIDO: Rótulo alterado para refletir a lógica correta)
        self.linha_sons = tk.Frame(self.form_frame, bg="#FFFFFF")
        self.linha_sons.pack(fill="x", pady=20)
        tk.Label(self.linha_sons, text="Ativar sons",
                 bg="#FFFFFF", font=fonte_labels).pack(side="left")
        self.chk_sons = tk.Checkbutton(
            self.linha_sons, bg="#FFFFFF", variable=self.var_sons,
            cursor="hand2", command=self._salvar_tudo_na_memoria
        )
        self.chk_sons.pack(side="right")

        # Linha 3 — Hidratação
        self.linha_hidra = tk.Frame(self.form_frame, bg="#FFFFFF")
        self.linha_hidra.pack(fill="x", pady=20)
        tk.Label(self.linha_hidra, text="Lembrete de hidratação:",
                 bg="#FFFFFF", font=fonte_labels).pack(side="left")

        self.chk_hidra = tk.Checkbutton(
            self.linha_hidra, bg="#FFFFFF", variable=self.var_hidratacao,
            cursor="hand2", command=self._atualizar_estado_hidratacao
        )
        self.chk_hidra.pack(side="right", padx=(15, 0))

        self.combo_frequencia = ttk.Combobox(
            self.linha_hidra,
            textvariable=self.var_frequencia_agua,
            values=["A cada 30 minutos", "A cada 1 hora", "A cada 2 horas"],
            state="readonly", font=("Helvetica", 14), width=18
        )
        self.combo_frequencia.pack(side="right")
        self.combo_frequencia.bind("<<ComboboxSelected>>",
                                   lambda e: self._salvar_tudo_na_memoria())

        self.btn_sair = tk.Button(
            self.conteudo_cartao, text="Sair", bg="#FFFFFF", fg="#1A1A1A",
            font=("Helvetica", 20), relief="flat", cursor="hand2",
            command=self._voltar
        )
        self.btn_sair.pack(pady=(60, 0))

    # ── TEMA ──────────────────────────────────────────────────────────────
    def _ao_clicar_no_tema(self):
        self._salvar_tudo_na_memoria()
        if self.app and hasattr(self.app, 'aplicar_tema_global'):
            self.app.aplicar_tema_global()

    def aplicar_tema(self, escuro: bool):
        cor_tela   = "#1E1E1E" if escuro else "#D9D9D9"
        cor_cartao = "#2D2D2D" if escuro else "#FFFFFF"
        cor_texto  = "#FFFFFF" if escuro else "#1A1A1A"
        cor_titulo = "#FFFFFF" if escuro else "#000000"
        cor_chk    = "#1E1E1E" if escuro else "#FFFFFF"

        self.configure(bg=cor_tela)
        self.contorno.configure(bg=cor_tela)
        self.barra_superior.configure(bg=cor_tela)
        self.lbl_titulo_barra.configure(bg=cor_tela, fg=cor_texto)
        self.btn_x.configure(bg=cor_tela, fg=cor_texto,
                              activebackground=cor_tela, activeforeground=cor_texto)

        self.cartao.configure(bg=cor_cartao)
        self.conteudo_cartao.configure(bg=cor_cartao)
        self.lbl_titulo_config.configure(bg=cor_cartao, fg=cor_titulo)
        self.form_frame.configure(bg=cor_cartao)

        for fill_line in [self.linha_tema, self.linha_sons, self.linha_hidra]:
            fill_line.configure(bg=cor_cartao)
            for filho in fill_line.winfo_children():
                if isinstance(filho, tk.Label):
                    filho.configure(bg=cor_cartao, fg=cor_texto)
                elif isinstance(filho, tk.Checkbutton):
                    filho.configure(
                        bg=cor_cartao, fg=cor_texto,
                        activebackground=cor_cartao, activeforeground=cor_texto,
                        selectcolor=cor_chk
                    )

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TCombobox",
                         fieldbackground=cor_cartao, background=cor_cartao,
                         foreground=cor_texto, selectbackground=cor_cartao,
                         selectforeground=cor_texto)

        self.btn_sair.configure(bg=cor_cartao, fg=cor_texto,
                                activebackground=cor_cartao, activeforeground=cor_texto)

    # ── HIDRATAÇÃO ────────────────────────────────────────────────────────
    def _atualizar_estado_hidratacao(self):
        if self.var_hidratacao.get():
            self.combo_frequencia.config(state="readonly")
        else:
            self.combo_frequencia.config(state="disabled")
        self._salvar_tudo_na_memoria()

    # ── PERSISTÊNCIA ──────────────────────────────────────────────────────
    def _salvar_tudo_na_memoria(self):
        if self.app:
            self.app.config_tema_escuro     = self.var_tema_escuro.get()
            self.app.config_sons            = self.var_sons.get()
            self.app.config_hidratacao      = self.var_hidratacao.get()
            self.app.config_frequencia_agua = self.var_frequencia_agua.get()

        try:
            import pygame
            if pygame.mixer.get_init():
                pygame.mixer.music.set_volume(1.0 if self.var_sons.get() else 0.0)
        except Exception:
            pass

    # ── NAVEGAÇÃO ─────────────────────────────────────────────────────────
    def _voltar(self):
        self._salvar_tudo_na_memoria()
        if self.app:
            self.app.show_page("home")