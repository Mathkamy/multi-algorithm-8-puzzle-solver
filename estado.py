class Estado:

    def __init__(self, estado, pai, movimento, profundidade, custo, chave):

        self.estado = estado

        self.pai = pai

        self.movimento = movimento

        self.profundidade = profundidade

        self.custo = custo

        self.chave = chave

        if self.estado:
            self.map = ''.join(str(e) for e in self.estado)

    def __eq__(self, other):
        return self.map == other.map

    def __lt__(self, other):
        return self.map < other.map
