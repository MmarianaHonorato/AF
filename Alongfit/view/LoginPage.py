import tkinter as tk
from controller.auth_controller import AuthController

class LoginPage(tk.Frame):
    def __init__(self, parent, app=None):
        super().__init__(parent, bg="#D9D9D9")
        self.app = app
        
        # Instancia o controlador de autenticação localmente
        self.auth_controller = AuthController()
        self._build()

    def _build(self):
        # 0. CONTORNO EXPANSIVO (Garante fundo cinza cobrindo tudo)
        self.contorno = tk.Frame(self, bg="#D9D9D9", width=1300, height=1400)
        self.contorno.pack(anchor="c", expand=True, fill="both")
        self.contorno.pack_propagate(False)

        # 1. BARRA SUPERIOR (Com botão X para fechar o programa)
        barra_superior = tk.Frame(self.contorno, bg="#D9D9D9")
        barra_superior.pack(fill="x", padx=30, pady=20)
        
        tk.Button(
            barra_superior, text="X", bg="#D9D9D9", fg="#1A1A1A", 
            font=("Helvetica", 20, "bold"), relief="flat", 
            cursor="hand2", command=self._fechar_aplicativo
        ).pack(side="right")

        # 2. CARTÃO BRANCO CENTRAL
        cartao = tk.Frame(self.contorno, bg="#FFFFFF")
        cartao.pack(expand=True, fill="both", padx=120, pady=(0, 80))

        conteudo_cartao = tk.Frame(cartao, bg="#FFFFFF", padx=60, pady=40)
        conteudo_cartao.pack(expand=True, fill="both")

        # Título principal do Cartão
        tk.Label(
            conteudo_cartao, text="Login", bg="#FFFFFF", fg="#000000", 
            font=("Helvetica", 32, "bold")
        ).pack(pady=(0, 30))

        # --- Campo: Email ---
        tk.Label(
            conteudo_cartao, text="Email:", bg="#FFFFFF", fg="#1A1A1A", 
            font=("Helvetica", 18, "bold"), anchor="w"
        ).pack(fill="x", pady=(10, 5))
        
        self.ent_email = tk.Entry(
            conteudo_cartao, font=("Helvetica", 16), bg="#F5F5F5", 
            relief="flat", highlightthickness=1, highlightbackground="#CCCCCC"
        )
        self.ent_email.pack(fill="x", ipady=8, pady=(0, 15))

        # --- Campo: Senha ---
        tk.Label(
            conteudo_cartao, text="Senha:", bg="#FFFFFF", fg="#1A1A1A", 
            font=("Helvetica", 18, "bold"), anchor="w"
        ).pack(fill="x", pady=(10, 5))
        
        self.ent_senha = tk.Entry(
            conteudo_cartao, font=("Helvetica", 16), bg="#F5F5F5", 
            show="*", relief="flat", highlightthickness=1, highlightbackground="#CCCCCC"
        )
        self.ent_senha.pack(fill="x", ipady=8, pady=(0, 10))

        # Label oculta para exibição de mensagens de erro
        self.lbl_erro = tk.Label(conteudo_cartao, text="", bg="#FFFFFF", fg="#FF3333", font=("Helvetica", 12, "bold"))
        self.lbl_erro.pack(pady=5)

        # 3. BOTÃO DE SUBMISSÃO (LOGIN)
        btn_login = tk.Button(
            conteudo_cartao, text="Login", bg="#FFFFFF", fg="#000000",
            font=("Helvetica", 20), relief="groove", bd=2, cursor="hand2",
            padx=30, command=self._executar_login
        )
        btn_login.pack(pady=(15, 0))

    def _executar_login(self):
        email = self.ent_email.get().strip()
        senha = self.ent_senha.get().strip()

        # Limpa o aviso de erro anterior
        self.lbl_erro.config(text="")

        # Validação simples antes de chamar o banco
        if not email or not senha:
            self.lbl_erro.config(text="Por favor, preencha todos os campos.")
            return

        # Executa a autenticação através do AuthController
        sucesso, mensagem = self.auth_controller.realizar_login(email, senha)

        if sucesso:
            # Captura o ID do usuário que acabou de logar
            id_usuario = self.auth_controller.identificador_usuario_ativo
            
            # CORRIGIDO: Print puramente textual sem emojis para evitar o erro no Windows terminal
            print(f"Login efetuado com sucesso! ID do usuario: {id_usuario}")
            
            # PASSA O ID PARA O APP.PY INICIALIZAR O SISTEMA GLOBAL
            if self.app:
                self.app.inicializar_sistema_pos_login(id_usuario)
        else:
            # Exibe o erro retornado (Ex: Email ou senha incorretos)
            self.lbl_erro.config(text=mensagem)

    def _fechar_aplicativo(self):
        if self.app:
            self.app.quit()