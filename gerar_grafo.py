# ----------------------------------------------------------------------------------------------------------- #

'''
Bibliotecas necessárias e variáveis globais
'''

import yaml
import networkx as nx
import json
from pyvis.network import Network
from PyQt5.QtWidgets import QApplication
import sys

# ----------------------------------------------------------------------------------------------------------- #

'''
Script para gerar o grafo a partir do docker-compose.yml
'''

with open("docker-compose.yml", "r") as f:
    compose = yaml.safe_load(f)

G = nx.Graph()

ips_roteadores = {}
nomes_roteadores = {}

for nome_servico, servico in compose['services'].items():
    if nome_servico.startswith("router"):
        nome_roteador = None
        ip_roteador = None
        for env in servico.get("environment", []):
            if env.startswith("rtr_nome="):
                nome_roteador = env.split("=", 1)[1]
            elif env.startswith("rtr_ip="):
                ip_roteador = env.split("=", 1)[1]
        if nome_roteador and ip_roteador:
            G.add_node(nome_roteador, type="router")
            ips_roteadores[ip_roteador] = nome_roteador
            nomes_roteadores[nome_servico] = nome_roteador

for nome_servico, servico in compose['services'].items():
    if nome_servico.startswith("router"):
        nome_roteador = None
        vizinhos = {}
        for env in servico.get("environment", []):
            if env.startswith("rtr_nome="):
                nome_roteador = env.split("=", 1)[1]
            elif env.startswith("vizinhanca="):
                viz = env.split("=", 1)[1]
                vizinhos = json.loads(viz.replace("'", '"'))
        for nome_vizinho in vizinhos:
            G.add_edge(nome_roteador, nome_vizinho)

for nome_servico, servico in compose['services'].items():
    if nome_servico.startswith("host"):
        nome_host = nome_servico.upper()
        ip_roteador = None
        for env in servico.get("environment", []):
            if env.startswith("rtr_ip="):
                ip_roteador = env.split("=", 1)[1]
        if ip_roteador and ip_roteador in ips_roteadores:
            roteador = ips_roteadores[ip_roteador]
            G.add_node(nome_host, type="host")
            G.add_edge(nome_host, roteador)

net = Network(notebook=True)

for node, data in G.nodes(data=True):
    if data['type'] == 'router':
        net.add_node(node, label=node, color='#c4c4c4', size=20)
    else:
        net.add_node(node, label=node, color='#cfdcef', size=20)

for u, v in G.edges():
    net.add_edge(u, v)

net.html = net.html.replace('<body>', ''' <body style="margin: 0; padding: 0; overflow: hidden; height: 100vh;"> <div id="my_network" style="width: 100%; height: 100%;"></div>
''')

app = QApplication(sys.argv)

net.show("network_graph.html")

sys.exit(app.exec_())