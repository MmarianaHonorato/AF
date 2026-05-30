import tkinter as tk
from tkinter import ttk
from datetime import datetime
import sys
import os

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

sys.path.append(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            ".."
        )
    )
)

from controller.estatisticas_controller import EstatisticasController


# =========================
# CORES
# =========================
BG_BRANCO = "white"
BG_CINZA_ESCURO = "#D9D9D9"
COR_TITULO = "#1A1A1A"
COR_TEXTO = "#444444"


class StatsPage(tk.Frame):

    def __init__(self, parent, app=None):
        super().__init__(parent, bg=BG_CINZA_ESCURO)

        self.app = app

        self.controller = EstatisticasController(
            self.app.id_usuario_logado
        )

        self._build()

    def _build(self):

        tk.Label(
            self,
            text="Estatísticas",
            bg=BG_CINZA_ESCURO,
            fg=COR_TITULO,
            font=("Helvetica", 24, "bold")
        ).pack(anchor="w", padx=20, pady=(20, 10))

        self.contorno = tk.Frame(self, bg=BG_BRANCO)
        self.contorno.pack(expand=True, fill="both", padx=20, pady=(0, 20))

        self._build_topo()
        self._build_grafico()

    def _build_topo(self):

        topo = tk.Frame(self.contorno, bg=BG_BRANCO)
        topo.pack(fill="x", padx=30, pady=20)

        tk.Label(
            topo,
            text="Selecionar mês:",
            bg=BG_BRANCO,
            fg=COR_TEXTO,
            font=("Helvetica", 12)
        ).pack(side="left")

        self.combo_mes = ttk.Combobox(
            topo,
            state="readonly",
            width=15
        )

        self.combo_mes["values"] = [str(i) for i in range(1, 13)]
        self.combo_mes.pack(side="left", padx=10)

        self.combo_mes.set(str(datetime.now().month))

        self.combo_mes.bind(
            "<<ComboboxSelected>>",
            self.atualizar_grafico
        )

    def _build_grafico(self):

        self.frame_grafico = tk.Frame(self.contorno, bg="white")
        self.frame_grafico.pack(fill="both", expand=True, padx=20, pady=20)

        self.criar_grafico()

    # =========================
    # GRÁFICO
    # =========================
    def criar_grafico(self):

        for widget in self.frame_grafico.winfo_children():
            widget.destroy()

        mes = self.combo_mes.get()

        dias, qtd_alongamentos, minutos = (
            self.controller.buscar_dados_mes(mes)
        )

        if not dias:
            tk.Label(
                self.frame_grafico,
                text="Nenhum dado encontrado neste mês",
                font=("Helvetica", 14),
                bg="white"
            ).pack(expand=True)
            return

        fig = Figure(figsize=(10, 5), dpi=100)
        ax = fig.add_subplot(111)

        x = list(range(len(dias)))
        largura = 0.35

        # Barra 1: quantidade
        ax.bar(
            [i - largura/2 for i in x],
            qtd_alongamentos,
            width=largura,
            label="Qtd. Alongamentos"
        )

        # Barra 2: tempo total
        ax.bar(
            [i + largura/2 for i in x],
            minutos,
            width=largura,
            label="Tempo Total (min)"
        )

        ax.set_title(f"Alongamentos - Mês {mes}")
        ax.set_xlabel("Dias")
        ax.set_ylabel("Quantidade / Minutos")

        ax.set_xticks(x)
        ax.set_xticklabels(dias)

        ax.grid(True, alpha=0.3)
        ax.legend()

        fig.tight_layout()

        canvas = FigureCanvasTkAgg(fig, master=self.frame_grafico)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    def atualizar_grafico(self, event=None):
        self.criar_grafico()