from controller.gerenciador_banco import GerenciadorBanco


class EstatisticasController:

    def __init__(self, identificador_usuario_ativo):
        self.banco_dados = GerenciadorBanco()
        self.identificador_usuario_ativo = identificador_usuario_ativo

    def carregar_resumo_sessao(self):
        total_pausas, pausas_concluidas = self.banco_dados.obter_estatisticas_pausas(
            self.identificador_usuario_ativo
        )

        total_alongamentos, tempo_total_segundos = self.banco_dados.obter_estatisticas_alongamentos(
            self.identificador_usuario_ativo
        )

        taxa_conclusao = 0
        if total_pausas > 0:
            taxa_conclusao = (pausas_concluidas / total_pausas) * 100

        return {
            "total_pausas_programadas": total_pausas,
            "pausas_realizadas": pausas_concluidas,
            "taxa_conclusao_percentagem": round(taxa_conclusao, 1),
            "total_alongamentos_feitos": total_alongamentos,
            "tempo_total_exercicio_minutos": tempo_total_segundos // 60
        }

    def buscar_dados_mes(self, mes):
        return self.banco_dados.buscar_dados_mes(
            self.identificador_usuario_ativo,
            mes
        )