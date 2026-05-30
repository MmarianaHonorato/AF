import sqlite3
import os
from model.Alongamento import Alongamento
from model.JornadaTrabalho import JornadaTrabalho

class GerenciadorBanco:
    def __init__(self, caminho_banco_dados="alongfit.db"):
        self.caminho_banco_dados = caminho_banco_dados
        self._inicializar_banco_se_necessario()

    def _inicializar_banco_se_necessario(self):
        import os
        from pathlib import Path
        
        # Se o arquivo do banco já existir na pasta, o sistema já foi iniciado antes.
        if os.path.exists(self.caminho_banco_dados):
            return

        print("Primeiro acesso detectado: Construindo o banco de dados local...")
        
        pasta_raiz = Path(__file__).resolve().parent.parent
        caminho_dados = pasta_raiz / 'dao' / 'Script_InsertDados.sql'
        
        import sqlite3
        with sqlite3.connect(self.caminho_banco_dados) as conexao_banco:
            cursor_banco = conexao_banco.cursor()
            try:
                # 1. CRIAMOS AS TABELAS DIRETAMENTE AQUI (Garante que não há erros de sintaxe!)
                cursor_banco.executescript("""
                    CREATE TABLE IF NOT EXISTS Usuario (
                        idUsuario INTEGER PRIMARY KEY AUTOINCREMENT,
                        nome VARCHAR(45) NOT NULL,
                        email VARCHAR(255) NOT NULL UNIQUE,
                        senha VARCHAR(255) NOT NULL,
                        dataNasc DATE NOT NULL
                    );

                    CREATE TABLE IF NOT EXISTS TipoDor (
                        idTipoDor INTEGER PRIMARY KEY AUTOINCREMENT,
                        nome VARCHAR(45) NOT NULL,
                        descricao VARCHAR(100),
                        regiao_corpo VARCHAR(45)
                    );

                    CREATE TABLE IF NOT EXISTS Alongamento (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        nome VARCHAR(45) NOT NULL,
                        descricao VARCHAR(45),
                        duracao INTEGER
                    );

                    CREATE TABLE IF NOT EXISTS recomendacao_along (
                        TipoDor_idTipoDor INTEGER,
                        Alongamento_idAl INTEGER,
                        Usuario_idUsuario INTEGER,
                        PRIMARY KEY (TipoDor_idTipoDor, Alongamento_idAl, Usuario_idUsuario)
                    );

                    CREATE TABLE IF NOT EXISTS HistoricoAlon (
                        idHisto INTEGER PRIMARY KEY AUTOINCREMENT,
                        alongamento_idAl INTEGER NOT NULL,
                        usuario_idUsuario INTEGER NOT NULL,
                        tipoDor_idTipoDor INTEGER NOT NULL,
                        inicio DATETIME NOT NULL,
                        tempoTotal INTEGER,
                        dataFim DATETIME
                    );

                    CREATE TABLE IF NOT EXISTS Pausas (
                        idPausas INTEGER PRIMARY KEY AUTOINCREMENT,
                        inicio DATETIME,
                        fim DATETIME,
                        concluida TEXT,
                        Usuario_idUsuario INTEGER
                    );

                    CREATE TABLE IF NOT EXISTS JornadaTrabalho (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        nome TEXT,
                        Tempo INTEGER,
                        tempoLembrete INTEGER,
                        desconforto INTEGER,
                        Usuario_idUsuario INTEGER,
                        inicioJornd DATETIME,
                        fimJornd DATETIME
                    );
                """)

                # 2. INSERIMOS OS DADOS DO SEU SCRIPT DE INSERTS
                if caminho_dados.exists():
                    with open(caminho_dados, 'r', encoding='utf-8') as arquivo_dados:
                        cursor_banco.executescript(arquivo_dados.read())
                else:
                    print(f"AVISO: Não encontrei o ficheiro {caminho_dados}")
                    
                conexao_banco.commit()
                print("✅ Banco de dados 'alongfit.db' criado com SUCESSO e sem erros de sintaxe!")
            except Exception as erro:
                print(f"❌ Erro ao tentar criar o banco de dados inicial: {erro}")

    def autenticar_usuario(self, email_digitado, senha_digitada):
        with sqlite3.connect(self.caminho_banco_dados) as conexao_banco:
            cursor_banco = conexao_banco.cursor()
            cursor_banco.execute("""
                SELECT idUsuario, nome 
                FROM Usuario 
                WHERE email = ? AND senha = ?
            """, (email_digitado, senha_digitada))
            
            usuario_encontrado = cursor_banco.fetchone()
            
            if usuario_encontrado:
                return {"id": usuario_encontrado[0], "nome": usuario_encontrado[1]}
            return None

    def registrar_usuario(self, usuario):
        with sqlite3.connect(self.caminho_banco_dados) as conexao_banco:
            cursor_banco = conexao_banco.cursor()
            cursor_banco.execute("""
                INSERT INTO Usuario (Nome, email, senha, dataNasc)
                VALUES (?, ?, ?, ?)
            """, (usuario.nome, usuario.email, usuario.senha, usuario.dataNasc))
            conexao_banco.commit()

    def registrar_inicio_jornada(self, jornada):
        with sqlite3.connect(self.caminho_banco_dados) as conexao_banco:
            cursor_banco = conexao_banco.cursor()
            cursor_banco.execute("""
                INSERT INTO JornadaTrabalho (inicioJornd, tempoLembrete, Usuario_idUsuario)
                VALUES (?, ?, ?)
            """, (jornada.inicioJornd, jornada.tempoLembrete, jornada.usuario_idUsuario))
            conexao_banco.commit()
            return cursor_banco.lastrowid

    def registrar_fim_jornada(self, id_jornada, data_hora_fim):
        with sqlite3.connect(self.caminho_banco_dados) as conexao_banco:
            cursor_banco = conexao_banco.cursor()
            cursor_banco.execute("""
                UPDATE JornadaTrabalho 
                SET fimJornd = ? 
                WHERE id = ?
            """, (data_hora_fim, id_jornada))
            conexao_banco.commit()

    def buscar_alongamentos_por_dor(self, identificador_tipo_dor, identificador_usuario):
        with sqlite3.connect(self.caminho_banco_dados) as conexao_banco:
            cursor_banco = conexao_banco.cursor()
            cursor_banco.execute("""
                SELECT a.id, a.nome, a.descricao, a.duracao
                FROM Alongamento a
                INNER JOIN recomendacao_along r ON a.id = r.alongamento_idAl
                WHERE r.TipoDor_idTipoDor = ? AND r.Usuario_idUsuario = ?
            """, (identificador_tipo_dor, identificador_usuario))
            
            linhas_retornadas = cursor_banco.fetchall()
            lista_alongamentos = []
            
            for linha in linhas_retornadas:
                lista_alongamentos.append(Alongamento(
                    id=linha[0], nome=linha[1], descricao=linha[2], duracao=linha[3]
                ))
            return lista_alongamentos

    def registrar_pausa_concluida(self, pausa):
        with sqlite3.connect(self.caminho_banco_dados) as conexao_banco:
            cursor_banco = conexao_banco.cursor()
            cursor_banco.execute("""
                INSERT INTO Pausas (inicio, fim, concluida, Usuario_idUsuario)
                VALUES (?, ?, ?, ?)
            """, (pausa.inicio, pausa.fim, pausa.concluida, pausa.usuario_idUsuario))
            conexao_banco.commit()

    def registrar_historico_alongamento(self, historico):
        with sqlite3.connect(self.caminho_banco_dados) as conexao_banco:
            cursor_banco = conexao_banco.cursor()
            cursor_banco.execute("""
                INSERT INTO HistoricoAlon (alongamento_idAl, Usuario_idUsuario, tipoDor_idTipoDor, Inicio, tempoTotal, dataFim)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (historico.alongamento_idAl, historico.usuario_idUsuario, historico.tipoDor_idTipoDor, historico.inicio, historico.tempoTotal, historico.dataFim))
            conexao_banco.commit()

    def obter_estatisticas_pausas(self, identificador_usuario):
        with sqlite3.connect(self.caminho_banco_dados) as conexao_banco:
            cursor_banco = conexao_banco.cursor()
            cursor_banco.execute("""
                SELECT COUNT(*), SUM(CASE WHEN concluida = 'concluida' THEN 1 ELSE 0 END)
                FROM Pausas
                WHERE Usuario_idUsuario = ?
            """, (identificador_usuario,))
            
            resultado = cursor_banco.fetchone()
            total_pausas = resultado[0] if resultado[0] else 0
            pausas_concluidas = resultado[1] if resultado[1] else 0
            return total_pausas, pausas_concluidas

    def obter_estatisticas_alongamentos(self, identificador_usuario):
        with sqlite3.connect(self.caminho_banco_dados) as conexao_banco:
            cursor_banco = conexao_banco.cursor()
            cursor_banco.execute("""
                SELECT COUNT(*), SUM(tempoTotal)
                FROM HistoricoAlon
                WHERE Usuario_idUsuario = ?
            """, (identificador_usuario,))
            
            resultado = cursor_banco.fetchone()
            total_alongamentos = resultado[0] if resultado[0] else 0
            tempo_total = resultado[1] if resultado[1] else 0
            return total_alongamentos, tempo_total

    # ==============================================================================
    # AS FUNÇÕES NOVAS ANEXADAS ABAIXO (Para o App não dar erro nas telas novas)
    # ==============================================================================

    def registrar_nova_tarefa(self, jornada):
        with sqlite3.connect(self.caminho_banco_dados) as conexao_banco:
            cursor_banco = conexao_banco.cursor()
            cursor_banco.execute("""
                INSERT INTO JornadaTrabalho (nome, Tempo, tempoLembrete, usuario_idUsuario, desconforto)
                VALUES (?, ?, ?, ?, ?)
            """, (jornada.nome, jornada.tempo, jornada.tempoLembrete, jornada.usuario_idUsuario, jornada.desconforto))
            conexao_banco.commit()
            return cursor_banco.lastrowid

    def buscar_jornadas_por_usuario(self, id_usuario):
        with sqlite3.connect(self.caminho_banco_dados) as conexao_banco:
            cursor_banco = conexao_banco.cursor()
            cursor_banco.execute("""
                SELECT id, nome, Tempo, tempoLembrete, desconforto FROM JornadaTrabalho 
                WHERE Usuario_idUsuario = ?
            """, (id_usuario,))
            linhas = cursor_banco.fetchall()
            tarefas = []
            for linha in linhas:
                tarefas.append({
                    "id": linha[0],
                    "nome": linha[1],
                    "horas": linha[2] if linha[2] is not None else 0,
                    "minutos": linha[3] if linha[3] is not None else 0,
                    "desconforto": linha[4] if linha[4] is not None else 0
                })
            return tarefas

    def atualizar_tarefa(self, id_jornada, horas, minutos, desconforto):
        with sqlite3.connect(self.caminho_banco_dados) as conexao_banco:
            cursor_banco = conexao_banco.cursor()
            cursor_banco.execute("""
                UPDATE JornadaTrabalho 
                SET Tempo = ?, tempoLembrete = ?, desconforto = ? 
                WHERE id = ?
            """, (horas, minutos, desconforto, id_jornada))
            conexao_banco.commit()
            
    def excluir_tarefa(self, id_jornada):
        with sqlite3.connect(self.caminho_banco_dados) as conexao_banco:
            cursor_banco = conexao_banco.cursor()
            cursor_banco.execute("""
                DELETE FROM JornadaTrabalho 
                WHERE id = ?
            """, (id_jornada,))
            conexao_banco.commit()

    def obter_dias_semana_com_alongamento(self, identificador_usuario):
        with sqlite3.connect(self.caminho_banco_dados) as conexao_banco:
            cursor_banco = conexao_banco.cursor()
            cursor_banco.execute("""
                SELECT DISTINCT strftime('%w', inicio) 
                FROM HistoricoAlon 
                WHERE usuario_idUsuario = ? AND tempoTotal IS NOT NULL
            """, (identificador_usuario,))
            linhas = cursor_banco.fetchall()
            return [int(linha[0]) for linha in linhas if linha[0] is not None]

    #MARIANA
    def buscar_dados_mes(self, id_usuario, mes):
        with sqlite3.connect(self.caminho_banco_dados) as conn:
            cur = conn.cursor()

            cur.execute("""
                SELECT
                    strftime('%d', inicio) as dia,
                    COUNT(*) as qtd_alongamentos,
                    SUM(tempoTotal) as minutos
                FROM HistoricoAlon
                WHERE usuario_idUsuario = ?
                  AND strftime('%m', inicio) = ?
                GROUP BY dia
                ORDER BY dia
            """, (id_usuario, f"{int(mes):02d}"))

            rows = cur.fetchall()

            dias = [r[0] for r in rows]
            qtd = [r[1] for r in rows]
            minutos = [r[2] if r[2] else 0 for r in rows]

            return dias, qtd, minutos