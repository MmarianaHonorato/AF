class HistoricoAlon:
    def __init__(self, idHisto, alongamento_idAl, usuario_idUsuario, tipoDor_idTipoDor, inicio, tempoTotal, dataFim):
        self.idHisto = idHisto
        self.alongamento_idAl = alongamento_idAl
        self.usuario_idUsuario = usuario_idUsuario
        self.tipoDor_idTipoDor = tipoDor_idTipoDor
        self.inicio = inicio
        self.tempoTotal = tempoTotal
        self.dataFim = dataFim

    @property
    def idHisto(self):
        return self._idHisto

    @idHisto.setter
    def idHisto(self, valor):
        self._idHisto = valor

    @property
    def alongamento_idAl(self):
        return self._alongamento_idAl

    @alongamento_idAl.setter
    def alongamento_idAl(self, valor):
        if valor is not None and int(valor) <= 0:
            raise ValueError("O ID do alongamento deve ser um número maior que zero.")
        self._alongamento_idAl = valor

    @property
    def usuario_idUsuario(self):
        return self._usuario_idUsuario

    @usuario_idUsuario.setter
    def usuario_idUsuario(self, valor):
        if valor is not None and int(valor) <= 0:
            raise ValueError("O ID do usuário deve ser um número maior que zero.")
        self._usuario_idUsuario = valor

    @property
    def tipoDor_idTipoDor(self):
        return self._tipoDor_idTipoDor

    @tipoDor_idTipoDor.setter
    def tipoDor_idTipoDor(self, valor):
        if valor is not None and int(valor) <= 0:
            raise ValueError("O ID da dor deve ser um número maior que zero.")
        self._tipoDor_idTipoDor = valor

    @property
    def inicio(self):
        return self._inicio

    @inicio.setter
    def inicio(self, valor):
        if not valor:
            raise ValueError("A data/hora de início é obrigatória.")
        self._inicio = valor

    @property
    def tempoTotal(self):
        return self._tempoTotal

    @tempoTotal.setter
    def tempoTotal(self, valor):
        if valor is not None and int(valor) < 0:
            raise ValueError("O tempo total não pode ser negativo.")
        self._tempoTotal = valor

    @property
    def dataFim(self):
        return self._dataFim

    @dataFim.setter
    def dataFim(self, valor):
        self._dataFim = valor