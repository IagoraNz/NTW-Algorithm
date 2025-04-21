import heapq

class LinkState:
    def __init__(self, roteadores):
        self.roteadores = roteadores
        self.grafo = {}
        
        for roteador in roteadores:
            self.grafo[roteador] = {}
            
    def add_link(self, rot1, rot2, custo):
        self.grafo[rot1][rot2] = custo
        self.grafo[rot2][rot1] = custo
        
    def printar_grafo(self):
        for roteador, links in self.grafo.items():
            print(f"[ROUTER] {roteador}: {links}")
            
roteadores = ['A', 'B', 'C', 'D', 'E']
rede = LinkState(roteadores)

rede.add_link('A', 'B', 1)
rede.add_link('A', 'C', 4)
rede.add_link('B', 'C', 2)
rede.add_link('B', 'D', 5)
rede.add_link('C', 'D', 1)
rede.add_link('C', 'E', 3)

rede.printar_grafo()