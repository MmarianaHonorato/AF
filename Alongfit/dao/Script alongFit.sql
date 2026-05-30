PRAGMA foreign_keys = ON;

-- =========================
-- TABELA Usuario
-- =========================
CREATE TABLE Usuario (
    idUsuario   INTEGER PRIMARY KEY AUTOINCREMENT,
    nome        VARCHAR(45)  NOT NULL,
    email       VARCHAR(255) NOT NULL UNIQUE,
    senha       VARCHAR(255) NOT NULL,
    dataNasc    DATE         NOT NULL
);

-- =========================
-- TABELA TipoDor
-- =========================
CREATE TABLE TipoDor (
    idTipoDor    INTEGER PRIMARY KEY AUTOINCREMENT,
    nome         VARCHAR(45)  NOT NULL,
    descricao    VARCHAR(100),
    regiao_corpo VARCHAR(45)
);

-- =========================
-- TABELA Alongamento
-- =========================
CREATE TABLE Alongamento (
    id       INTEGER PRIMARY KEY AUTOINCREMENT,
    nome     VARCHAR(45) NOT NULL,
    descricao VARCHAR(45),
    duracao  INTEGER
);

-- =========================
-- TABELA recomendacao_along
-- =========================
CREATE TABLE recomendacao_along (
    tipoDor_idTipoDor   INTEGER NOT NULL,
    alongamento_idAl    INTEGER NOT NULL,

    PRIMARY KEY (
        tipoDor_idTipoDor,
        alongamento_idAl,
        
    ),

    FOREIGN KEY (tipoDor_idTipoDor)
        REFERENCES TipoDor(idTipoDor)
        ON DELETE CASCADE ON UPDATE CASCADE,

    FOREIGN KEY (alongamento_idAl)
        REFERENCES Alongamento(id)
        ON DELETE CASCADE ON UPDATE CASCADE,
);
-- =========================
-- TABELA HistoricoAlon
-- =========================
CREATE TABLE HistoricoAlon (
    idHisto             INTEGER PRIMARY KEY AUTOINCREMENT,
    alongamento_idAl    INTEGER  NOT NULL,
    usuario_idUsuario   INTEGER  NOT NULL,
    tipoDor_idTipoDor   INTEGER  NOT NULL,
    inicio              DATETIME NOT NULL,
    tempoTotal          INTEGER,
    dataFim             DATETIME,
    FOREIGN KEY (alongamento_idAl)
        REFERENCES Alongamento(id)
        ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (usuario_idUsuario)
        REFERENCES Usuario(idUsuario)
        ON DELETE CASCADE ON UPDATE CASCADE
);

-- =========================
-- TABELA JornadaTrabalho
-- =========================
CREATE TABLE JornadaTrabalho (
    id                INTEGER PRIMARY KEY AUTOINCREMENT,
    nome              VARCHAR(100) NOT NULL,
    Tempo             INTEGER NOT NULL, -- Corrigido para INTEGER (para guardar 4, 6, 8)
    tempoLembrete     INTEGER NOT NULL,
    usuario_idUsuario INTEGER NOT NULL,
    desconforto       INTEGER,          -- Corrigido para INTEGER (Chave Estrangeira do ID da Dor)
    FOREIGN KEY (usuario_idUsuario)
        REFERENCES Usuario(idUsuario)
        ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (desconforto)
        REFERENCES TipoDor(idTipoDor)
        ON DELETE SET NULL ON UPDATE CASCADE
);

-- =========================
-- TABELA Pausas
-- =========================
CREATE TABLE Pausas (
    idPausas          INTEGER PRIMARY KEY AUTOINCREMENT,
    inicio            DATETIME,
    fim               DATETIME,
    concluida         VARCHAR(20) CHECK(concluida IN ('concluida','ignorada','pendente')),
    usuario_idUsuario INTEGER NOT NULL,
    FOREIGN KEY (usuario_idUsuario)
        REFERENCES Usuario(idUsuario)
        ON DELETE CASCADE ON UPDATE CASCADE
);