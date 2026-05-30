import tkinter as tk
from pathlib import Path
import pygame

from datetime import timedelta, datetime
from controller.gerenciador_banco import GerenciadorBanco
from model.Pausas import Pausas
from model.HistoricoAlon import HistoricoAlon
from model.Alongamento import Alongamento
from view.pop_up import PopUp


class SessaoController:
    def __init__(self, janela_principal, identificador_usuario_logado):
        self.janela_principal            = janela_principal
        self.identificador_usuario_logado = identificador_usuario_logado
        self.banco_dados                 = GerenciadorBanco()

        self.tempo_trabalho_total_restante  = 0
        self.tempo_pausa_segundos           = 0
        self.tempo_restante_segundos        = 0

        self.identificador_dor_selecionada       = None
        self.temporizador_rodando                = False
        self.identificador_processo_temporizador = None

        self.funcao_atualizar_texto_relogio = None
        self.funcao_atualizar_tempo_total   = None

        self._processo_hidratacao = None

        try:
            pygame.mixer.init()
        except Exception:
            pass

    # ── CONFIGURAÇÃO DA SESSÃO ────────────────────────────────────────────
    def configurar_sessao(self, horas_trabalho, minutes_pausa, identificador_dor):
        self.tempo_trabalho_total_restante = horas_trabalho * 3600
        self.tempo_pausa_segundos          = minutes_pausa * 60
        self.identificador_dor_selecionada = identificador_dor
        self._definir_proximo_ciclo()

    def _definir_proximo_ciclo(self):
        if self.tempo_trabalho_total_restante > self.tempo_pausa_segundos:
            self.tempo_restante_segundos = self.tempo_pausa_segundos
        else:
            self.tempo_restante_segundos = self.tempo_trabalho_total_restante
        self.atualizar_interface_relogio()

    # ── VINCULAÇÃO DE INTERFACE ───────────────────────────────────────────
    def vincular_interface_relogio(self, funcao_atualizacao):
        self.funcao_atualizar_texto_relogio = funcao_atualizacao
        self.atualizar_interface_relogio()

    def vincular_interface_tempo_total(self, funcao_atualizacao):
        self.funcao_atualizar_tempo_total = funcao_atualizacao
        self.atualizar_interface_relogio()

    def obter_progresso_semanal(self):
        return self.banco_dados.obter_dias_semana_com_alongamento(
            self.identificador_usuario_logado
        )

    # ── TEMPORIZADOR ─────────────────────────────────────────────────────
    def iniciar_temporizador(self):
        if not self.temporizador_rodando:
            self.temporizador_rodando = True
            self.executar_ciclo_temporizador()
            self._iniciar_lembrete_hidratacao()

    def pausar_temporizador(self):
        self.temporizador_rodando = False
        if self.identificador_processo_temporizador is not None:
            self.janela_principal.after_cancel(self.identificador_processo_temporizador)
            self.identificador_processo_temporizador = None
        self._cancelar_lembrete_hidratacao()

    def executar_ciclo_temporizador(self):
        if self.temporizador_rodando and self.tempo_restante_segundos > 0:
            self.tempo_restante_segundos       -= 1
            self.tempo_trabalho_total_restante -= 1
            self.atualizar_interface_relogio()
            self.identificador_processo_temporizador = self.janela_principal.after(
                1000, self.executar_ciclo_temporizador
            )
        elif self.tempo_restante_segundos <= 0:
            self.pausar_temporizador()
            if self.tempo_trabalho_total_restante <= 0:
                self.finalizar_jornada_completa()
            else:
                self.disparar_alerta_alongamento()

    def ticar_tempo_total_durante_alongamento(self):
        if self.tempo_trabalho_total_restante > 0:
            self.tempo_trabalho_total_restante -= 1
            self.atualizar_interface_relogio()
            if self.tempo_trabalho_total_restante <= 0:
                self.finalizar_jornada_completa()

    def atualizar_interface_relogio(self):
        if self.funcao_atualizar_texto_relogio:
            t = str(timedelta(seconds=self.tempo_restante_segundos))
            if t.startswith("0:"):
                t = t[2:]
            self.funcao_atualizar_texto_relogio(t)
        if self.funcao_atualizar_tempo_total:
            self.funcao_atualizar_tempo_total(
                str(timedelta(seconds=max(0, self.tempo_trabalho_total_restante)))
            )

    # ── ALERTA DE ALONGAMENTO ─────────────────────────────────────────────
    def disparar_alerta_alongamento(self):
        sons_ativados = getattr(self.janela_principal, 'config_sons', True)

        if sons_ativados:
            try:
                caminho_som = (
                    Path(__file__).resolve().parent.parent / "assets" / "new-ford-chime.mp3"
                )
                if caminho_som.exists():
                    pygame.mixer.music.load(str(caminho_som))
                    pygame.mixer.music.play()
                else:
                    print(f"Aviso: Som não encontrado em {caminho_som}")
            except Exception as e:
                print(f"Log: Erro ao tocar o som ({e})")
        else:
            print("Log: Alarme silenciado — opção 'Sons' desativada.")

        alongamentos = self.banco_dados.buscar_alongamentos_por_dor(
            self.identificador_dor_selecionada,
            self.identificador_usuario_logado
        )

        if not alongamentos:
            nomes = {0: "Geral", 1: "Ombros/Pescoço", 4: "Mãos/Punhos", 5: "Costas"}
            regiao = nomes.get(self.identificador_dor_selecionada, "Corpo")
            alongamento = Alongamento(
                id=999, nome=f"Alongamento para {regiao}",
                descricao="Afaste-se da cadeira, estique os braços para cima e relaxe o pescoço.",
                duracao=30
            )
        else:
            alongamento = alongamentos[0]

        try:
            agora  = datetime.now()
            fim    = agora + timedelta(seconds=alongamento.duracao)
            ini_fmt = agora.strftime("%Y-%m-%d %H:%M:%S")
            fim_fmt = fim.strftime("%Y-%m-%d %H:%M:%S")

            self.banco_dados.registrar_pausa_concluida(Pausas(
                idPausas=None, inicio=ini_fmt, fim=fim_fmt,
                concluida='concluida',
                usuario_idUsuario=self.identificador_usuario_logado
            ))
            if alongamento.id != 999:
                self.banco_dados.registrar_historico_alongamento(HistoricoAlon(
                    idHisto=None,
                    alongamento_idAl=alongamento.id,
                    usuario_idUsuario=self.identificador_usuario_logado,
                    tipoDor_idTipoDor=self.identificador_dor_selecionada,
                    inicio=ini_fmt, tempoTotal=alongamento.duracao, dataFim=fim_fmt
                ))
        except Exception as e:
            print(f"Log: Pausa registrada localmente ({e})")

        PopUp(self.janela_principal, controller=self, alongamento=alongamento)

    def retomar_apos_alongamento(self):
        if self.tempo_trabalho_total_restante <= 0:
            self.finalizar_jornada_completa()
            return
        self._definir_proximo_ciclo()
        self.iniciar_temporizador()

    def finalizar_jornada_completa(self):
        self.temporizador_rodando = False
        self._cancelar_lembrete_hidratacao()
        if self.funcao_atualizar_texto_relogio:
            self.funcao_atualizar_texto_relogio("00:00")
        if self.funcao_atualizar_tempo_total:
            self.funcao_atualizar_tempo_total("0:00:00")

    # ── LEMBRETE DE HIDRATAÇÃO ────────────────────────────────────────────
    def _obter_intervalo_hidratacao_ms(self):
        frequencia = getattr(self.janela_principal, 'config_frequencia_agua', "A cada 1 hora")
        mapa = {
            "A cada 30 minutos": 30 * 60 * 1000,
            "A cada 1 hora":     60 * 60 * 1000,
            "A cada 2 horas":   120 * 60 * 1000,
        }
        return mapa.get(frequencia, 60 * 60 * 1000)

    def _iniciar_lembrete_hidratacao(self):
        self._cancelar_lembrete_hidratacao()
        if getattr(self.janela_principal, 'config_hidratacao', False):
            self._processo_hidratacao = self.janela_principal.after(
                self._obter_intervalo_hidratacao_ms(),
                self._disparar_lembrete_agua
            )

    def _cancelar_lembrete_hidratacao(self):
        if self._processo_hidratacao is not None:
            self.janela_principal.after_cancel(self._processo_hidratacao)
            self._processo_hidratacao = None

    def _disparar_lembrete_agua(self):
        if not getattr(self.janela_principal, 'config_hidratacao', False):
            return
        self._mostrar_popup_agua()
        self._processo_hidratacao = self.janela_principal.after(
            self._obter_intervalo_hidratacao_ms(),
            self._disparar_lembrete_agua
        )

    def _mostrar_popup_agua(self):
        try:
            popup = tk.Toplevel(self.janela_principal)
            popup.title("💧 Hora de beber água!")
            popup.resizable(False, False)
            popup.grab_set()

            popup.update_idletasks()
            largura, altura = 340, 180
            x = (popup.winfo_screenwidth()  - largura) // 2
            y = (popup.winfo_screenheight() - altura)  // 2
            popup.geometry(f"{largura}x{altura}+{x}+{y}")

            escuro    = getattr(self.janela_principal, 'config_tema_escuro', False)
            cor_fundo = "#2D2D2D" if escuro else "#FFFFFF"
            cor_texto = "#FFFFFF" if escuro else "#1A1A1A"
            popup.configure(bg=cor_fundo)

            tk.Label(popup, text="💧 Hora de beber água!",
                     bg=cor_fundo, fg=cor_texto,
                     font=("Helvetica", 16, "bold")).pack(pady=(28, 8))
            tk.Label(popup, text="Pare um instante e hidrate-se.",
                     bg=cor_fundo, fg=cor_texto,
                     font=("Helvetica", 13)).pack()
            tk.Button(popup, text="Ok, obrigado!",
                      bg="#4A9EFF", fg="#FFFFFF",
                      font=("Helvetica", 13, "bold"),
                      relief="flat", cursor="hand2", padx=20, pady=8,
                      command=popup.destroy).pack(pady=24)
        except Exception as e:
            print(f"Log: Não foi possível exibir o popup de hidratação ({e})")
