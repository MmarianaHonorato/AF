class Pausas:
    def __init__(self, idPausas, inicio, fim, concluida, usuario_idUsuario):
        self.idPausas = idPausas
        self.inicio = inicio
        self.fim = fim
        self.concluida = concluida
        self.usuario_idUsuario = usuario_idUsuario

    @property
    def idPausas(self):
        return self._idPausas

    @idPausas.setter
    def idPausas(self, valor):
        self._idPausas = valor

    @property
    def inicio(self):
        return self._inicio

    @inicio.setter
    def inicio(self, valor):
        if not valor:
            raise ValueError("O horário de início da pausa é obrigatório.")
        self._inicio = valor

    @property
    def fim(self):
        return self._fim

    @fim.setter
    def fim(self, valor):
        self._fim = valor

    @property
    def concluida(self):
        return self._concluida

    @concluida.setter
    def concluida(self, valor):
        opcoes_validas = ['concluida', 'ignorada', 'pendente']
        if valor in opcoes_validas:
            self._concluida = valor
        else:
            raise ValueError("O status de conclusão deve ser 'concluida', 'ignorada' ou 'pendente'.")

    @property
    def usuario_idUsuario(self):
        return self._usuario_idUsuario

    @usuario_idUsuario.setter
    def usuario_idUsuario(self, valor):
        if valor is not None and int(valor) <= 0:
            raise ValueError("O ID do usuário deve ser um número válido.")
        self._usuario_idUsuario = valor