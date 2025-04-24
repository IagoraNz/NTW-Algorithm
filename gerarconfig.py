# -------------------------------------------------------------------------------------------------- #

'''
Bibliotecas utilizadas
'''

import networkx as nx
import random
import yaml
import matplotlib.pyplot as plt

# -------------------------------------------------------------------------------------------------- #

'''
Variáveis globais
'''

nRoteadores = 6
hostsPorRoteador = 2
grauMin = 3

# -------------------------------------------------------------------------------------------------- #

'''
Configurações
'''

def geraGrafo(n, min_deg):
    """
    Essa função gera um grafo conectado aleatório com n nós e grau mínimo min_deg.

    Args:
        n (int): Número de nós no grafo.
        min_deg (int): Grau mínimo desejado para cada nó.

    Returns:
        G (networkx.Graph): Um grafo conectado aleatório com n nós e grau mínimo min_deg.
    """
    while True:
        p = random.uniform(0.4, 0.6)
        G = nx.erdos_renyi_graph(n, p)

        if nx.is_connected(G) and all(G.degree(n) >= min_deg for n in G.nodes()):
            return G

grafo = geraGrafo(nRoteadores, grauMin)

for (u, v) in grafo.edges():
    grafo.edges[u, v]['weight'] = random.randint(2, 15)

compose = {
    'services': {},
    'networks': {}
}

contSubnet = 10
contp2p = 100

for r in grafo.nodes():
    nomeRoteador = f"r{r+1}".lower()
    redesRoteador = []
    
    for h in range(hostsPorRoteador):
        nome_host = f"h{r+1}_{h+1}".lower()
        nome_net = f"net_r{r+1}_h{h+1}".lower()
        subnet = f"172.16.{contSubnet}.0/24"
        ip_host = f"172.16.{contSubnet}.100"
        ip_router = f"172.16.{contSubnet}.1"

        compose['services'][nome_host] = {
            'build': './host',
            'container_name': nome_host,
            'image': f"ntw-algorithm-1-{nome_host}",
            'networks': {
                nome_net: {
                    'ipv4_address': ip_host
                }
            }
        }

        compose['networks'][nome_net] = {
            'driver': 'bridge',
            'ipam': {
                'config': [{'subnet': subnet}]
            }
        }

        redesRoteador.append({
            nome_net: {'ipv4_address': ip_router}
        })

        contSubnet += 1

    compose['services'][nomeRoteador] = {
        'build': './router',
        'container_name': nomeRoteador,
        'image': f"ntw-algorithm-1-{nomeRoteador}",
        'networks': {}
    }

    for net in redesRoteador:
        compose['services'][nomeRoteador]['networks'].update(net)

for (u, v, d) in grafo.edges(data=True):
    nome_net = f"p2p_r{u+1}_r{v+1}".lower()
    subnet = f"10.0.{contp2p}.0/30"
    ip_u = f"10.0.{contp2p}.1"
    ip_v = f"10.0.{contp2p}.2"

    compose['networks'][nome_net] = {
        'driver': 'bridge',
        'ipam': {
            'config': [{'subnet': subnet}]
        }
    }

    compose['services'][f"r{u+1}".lower()]['networks'][nome_net] = {
        'ipv4_address': ip_u
    }
    compose['services'][f"r{v+1}".lower()]['networks'][nome_net] = {
        'ipv4_address': ip_v
    }

    contp2p += 1

with open('docker-compose.yml', 'w') as f:
    yaml.dump(compose, f, sort_keys=False)

print("[CHECK] docker-compose.yml gerado com sucesso!")

# -------------------------------------------------------------------------------------------------- #

'''
Criação do grafo para visualização
'''

visual_graph = nx.Graph()

for r in grafo.nodes():
    nomeRoteador = f"r{r+1}".lower()
    visual_graph.add_node(nomeRoteador, type='router')
    for h in range(hostsPorRoteador):
        nome_host = f"h{r+1}_{h+1}".lower()
        visual_graph.add_node(nome_host, type='host')
        visual_graph.add_edge(nomeRoteador, nome_host)

for (u, v) in grafo.edges():
    visual_graph.add_edge(f"r{u+1}".lower(), f"r{v+1}".lower())

node_colors = [
    '#555555' if data['type'] == 'router' else '#99ccff'
    for _, data in visual_graph.nodes(data=True)
]

# -------------------------------------------------------------------------------------------------- #

'''
Visualização do grafo
'''

plt.figure(figsize=(12, 10))
pos = nx.spring_layout(visual_graph, seed=123)
nx.draw(
    visual_graph,
    pos,
    with_labels=True,
    node_color=node_colors,
    node_size=2000,
    font_size=8,
    font_weight='bold',
    edge_color='darkgray',
    width=2
)
plt.title("Topologia Aleatória de Rede com Roteadores e Hosts")
plt.savefig('network_topology.png')

# -------------------------------------------------------------------------------------------------- #