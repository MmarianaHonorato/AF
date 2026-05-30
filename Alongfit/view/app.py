import sys
import os
import tkinter as tk

caminho_raiz = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(caminho_raiz)

from controller.config_controller import ConfigController
from controller.sessao_controller import SessaoController

from alongamento_page import AlongamentoPage
from config_page import ConfigPage
from home_page import HomePage
from sidebar import Sidebar
from stats_page import StatsPage
from timer_page import TimerPage
from LoginPage import LoginPage  # <--- IMPORTAÇÃO DA NOVA TELA AQUI

PAGES = {
    "login": LoginPage,         # <--- MAPEAMENTO DA TELA DE LOGIN
    "home": HomePage,
    "stats": StatsPage,
    "timer": TimerPage,
    "config": ConfigPage,
    "alongamento": AlongamentoPage,
}

# Páginas que recebem `app=self`
PAGES_COM_APP = {"login", "home", "timer", "alongamento", "config", "stats"}


def rodar_app():
    app = AlongFitApp()
    app.mainloop()


class AlongFitApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("AlongFit")
        self.geometry("700x450")
        self.minsize(500, 350)
        self.configure(bg="#FFFFFF")

        # ── Configurações globais de UI (persistem entre páginas) ──────────
        self.config_tema_escuro     = False
        self.config_sons            = True
        self.config_hidratacao      = False
        self.config_frequencia_agua = "A cada 1 hora"

        # ── Estado de Autenticação Inicial ──────────────────────────────────
        self.id_usuario_logado = None  # Começa vazio (Deslogado)

        # controladores globais iniciam como None e nascem pós-login
        self.config_controller = None
        self.sessao_controller = None

        # ── Inicializa a Sidebar (Mas NÃO empacota ainda para ficar oculta) ──
        self.sidebar = Sidebar(self, on_select=self.show_page, active_page="home")

        # ── Área de conteúdo expansiva ──────────────────────────────────────
        self.content = tk.Frame(self, bg="#FFFFFF")
        self.content.pack(side="right", fill="both", expand=True)

        self.current_page = None
        
        # Força o aplicativo a abrir direto na tela de Login!
        self.show_page("login")

    # ═══════════════════════════════════════════════════════════════════════
    # GATILHO MÁGICO PÓS-AUTENTICAÇÃO
    # Chamado pela LoginPage passando o ID real do Banco de Dados
    # ═══════════════════════════════════════════════════════════════════════
    def inicializar_sistema_pos_login(self, id_usuario):
        """Monta a estrutura real do app baseada no Usuário Autenticado"""
        self.id_usuario_logado = id_usuario
        
        # Acorda os controladores reais associados ao ID correto
        self.config_controller = ConfigController(self.id_usuario_logado)
        self.sessao_controller = SessaoController(self, self.id_usuario_logado)
        
        # Reorganiza o layout para injetar a Sidebar à esquerda de forma fixa
        self.content.pack_forget()
        self.sidebar.pack(side="left", fill="y")
        self.content.pack(side="right", fill="both", expand=True)
        
        # Redireciona o fluxo do usuário para a Home do AlongFit
        self.show_page("home")

    # ═══════════════════════════════════════════════════════════════════════
    # NAVEGAÇÃO
    # ═══════════════════════════════════════════════════════════════════════
    def show_page(self, page_name):
        if self.current_page is not None:
            self.current_page.destroy()

        page_class = PAGES[page_name]
        self.current_page = page_class(self.content, app=self)
        self.current_page.pack(fill="both", expand=True)

        # Aplica o tema logo após criar a página
        self.aplicar_tema_global()

    # ═══════════════════════════════════════════════════════════════════════
    # TEMA GLOBAL
    # ═══════════════════════════════════════════════════════════════════════
    def aplicar_tema_global(self):
        escuro = self.config_tema_escuro

        cor_raiz    = "#1E1E1E" if escuro else "#FFFFFF"
        cor_sidebar = "#2D2D2D" if escuro else "#FFFFFF"
        cor_content = "#1E1E1E" if escuro else "#FFFFFF"

        # Janela raiz e container de conteúdo
        self.configure(bg=cor_raiz)
        self.content.configure(bg=cor_content)

        # Sidebar
        if hasattr(self.sidebar, 'aplicar_tema'):
            self.sidebar.aplicar_tema(escuro)

        # Página atual (se ela souber se tematizar)
        if self.current_page and hasattr(self.current_page, 'aplicar_tema'):
            self.current_page.aplicar_tema(escuro)


if __name__ == "__main__":
    try:
        import hupper
        print("Hot Reload Ativo! Monitorando alterações...")
        reloader = hupper.start_reloader("app.rodar_app")
    except ImportError:
        rodar_app()