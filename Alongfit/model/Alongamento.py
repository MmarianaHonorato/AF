class Alongamento:
    def __init__(self, id, nome, descricao, duracao):
        self.id = id
        self.nome = nome
        self.descricao = descricao
        self.duracao = duracao

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, valor):
        self._id = valor

    @property
    def nome(self):
        return self._nome

    @nome.setter
    def nome(self, valor):
        if not valor or str(valor).strip() == "":
            raise ValueError("O nome do alongamento não pode ser vazio.")
        self._nome = valor

    @property
    def descricao(self):
        return self._descricao

    @descricao.setter
    def descricao(self, valor):
        self._descricao = valor if valor else ""

    @property
    def duracao(self):
        return self._duracao

    @duracao.setter
    def duracao(self, valor):
        if valor is not None and int(valor) <= 0:
            raise ValueError("A duração do alongamento deve ser maior que zero segundos.")
        self._duracao = valor

    @property
    def historicos(self):
        return self._historicos

    @historicos.setter
    def historicos(self, valor):
        if not isinstance(valor, list):
            raise TypeError("Históricos deve ser uma lista.")
        self._historicos = valor

    @property
    def recomendacoes(self):
        return self._recomendacoes

    @recomendacoes.setter
    def recomendacoes(self, valor):
        if not isinstance(valor, list):
            raise TypeError("Recomendações deve ser uma lista.")
        self._recomendacoes = valor
