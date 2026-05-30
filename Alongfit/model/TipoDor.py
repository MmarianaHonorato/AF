class TipoDor:
    def __init__(self, idTipoDor, nome, descricao, regiao_corpo):
        self.idTipoDor = idTipoDor
        self.nome = nome
        self.descricao = descricao
        self.regiao_corpo = regiao_corpo

    @property
    def idTipoDor(self):
        return self._idTipoDor

    @idTipoDor.setter
    def idTipoDor(self, valor):
        self._idTipoDor = valor

    @property
    def nome(self):
        return self._nome

    @nome.setter
    def nome(self, valor):
        if not valor or str(valor).strip() == "":
            raise ValueError("O nome do tipo de dor não pode ser vazio.")
        self._nome = valor

    @property
    def descricao(self):
        return self._descricao

    @descricao.setter
    def descricao(self, valor):
        self._descricao = valor if valor else ""

    @property
    def regiao_corpo(self):
        return self._regiao_corpo

    @regiao_corpo.setter
    def regiao_corpo(self, valor):
        if not valor or str(valor).strip() == "":
            raise ValueError("A região do corpo associada à dor deve ser especificada.")
        self._regiao_corpo = valor
