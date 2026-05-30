from datetime import datetime
from model.JornadaTrabalho import JornadaTrabalho
from controller.gerenciador_banco import GerenciadorBanco

class ConfigController:
    def __init__(self, identificador_usuario_ativo):
        self.banco_dados = GerenciadorBanco()
        self.identificador_usuario_ativo = identificador_usuario_ativo

    def salvar_preferencias_e_iniciar_jornada(self, horas_trabalho, minutos_pausa):
        try:
            data_hora_atual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            nova_jornada = JornadaTrabalho(
                id=None,
                inicioJornd=data_hora_atual,
                tempoLembrete=minutos_pausa,
                usuario_idUsuario=self.identificador_usuario_ativo,
                fimJornd=None
            )
            
            id_jornada_criada = self.banco_dados.registrar_inicio_jornada(nova_jornada)
            
            return True, "Configurações salvas e jornada iniciada com sucesso.", id_jornada_criada
            
        except ValueError as erro_validacao:
            return False, str(erro_validacao), None
            
        except Exception:
            return False, "Erro inesperado ao salvar no banco de dados.", None
        
    def buscar_tarefas_do_usuario(self):
        """Pede ao banco de dados todas as tarefas/jornadas pendentes deste usuário"""
        return self.banco_dados.buscar_jornadas_por_usuario(self.identificador_usuario_ativo)

    def salvar_nova_tarefa(self, nome_tarefa, horas, minutos):
        """Salva uma tarefa nova como 'Pendente' (sem data de início ainda)"""
        try:
            # Aqui estamos a criar a jornada, mas sem iniciar o tempo ainda
            nova_jornada = JornadaTrabalho(
                id=None,
                inicioJornd=None, # Só vai preencher quando clicar em "Iniciar"
                nome=nome_tarefa,
                tempoLembrete=minutos,
                usuario_idUsuario=self.identificador_usuario_ativo,
                fimJornd=None
            )
            
            # Adicione 'horas_trabalho' no modelo Jornada se quiser salvar no BD também!
            id_criado = self.banco_dados.registrar_nova_tarefa(nova_jornada)
            
            return True, "Tarefa salva com sucesso", id_criado
        except Exception as e:
            return False, f"Erro ao salvar: {str(e)}", None
        
    def salvar_nova_tarefa(self, nome_tarefa, horas, minutos, id_dor):
        try:
            nova_jornada = JornadaTrabalho(
                id=None,
                nome=nome_tarefa,
                tempo=horas,
                tempoLembrete=minutos,
                usuario_idUsuario=self.identificador_usuario_ativo,
                desconforto=id_dor
            )
            id_criado = self.banco_dados.registrar_nova_tarefa(nova_jornada)
            return True, "Tarefa salva com sucesso", id_criado
        except Exception as e:
            return False, f"Erro ao salvar: {str(e)}", None

    def atualizar_tarefa_existente(self, id_jornada, horas, minutos, id_dor):
        self.banco_dados.atualizar_tarefa(id_jornada, horas, minutos, id_dor)
    
    def excluir_tarefa(self, id_jornada):
        """Pede ao banco de dados para excluir uma tarefa específica"""
        try:
            self.banco_dados.excluir_tarefa(id_jornada)
            return True, "Tarefa excluída com sucesso"
        except Exception as e:
            return False, f"Erro ao excluir: {str(e)}"