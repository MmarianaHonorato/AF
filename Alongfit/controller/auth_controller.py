from model.Usuario import Usuario
from controller.gerenciador_banco import GerenciadorBanco

class AuthController:
    def __init__(self):
        self.banco_dados = GerenciadorBanco()
        self.identificador_usuario_ativo = None
        self.nome_usuario_ativo = None

    def realizar_login(self, email_digitado, senha_digitada):
        usuario_encontrado = self.banco_dados.autenticar_usuario(email_digitado, senha_digitada)
        
        if usuario_encontrado:
            self.identificador_usuario_ativo = usuario_encontrado["id"]
            self.nome_usuario_ativo = usuario_encontrado["nome"]
            return True, "Login realizado com sucesso."
            
        return False, "Email ou senha incorretos."

    def realizar_cadastro(self, nome_digitado, email_digitado, senha_digitada, data_nascimento_digitada):
        try:
            novo_usuario = Usuario(
                idUsuario=None,
                nome=nome_digitado,
                email=email_digitado,
                senha=senha_digitada,
                dataNasc=data_nascimento_digitada
            )
            
            self.banco_dados.registrar_usuario(novo_usuario)
            return True, "Cadastro realizado com sucesso."
            
        except ValueError as erro_validacao:
            return False, str(erro_validacao)
            
        except Exception:
            return False, "Erro ao registrar no banco de dados. O email já pode estar em uso."

    def deslogar_usuario(self):
        self.identificador_usuario_ativo = None
        self.nome_usuario_ativo = None