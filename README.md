# 📄 Implementação do primeiro trabalgo da disciplina de Redes de Computadores II.

## 🔗 Objetivo
Desenvolver uma simulação de uma rede de computadores composta por hosts e roteadores utilizando Python e Docker, onde os roteadores implementam o algoritmo de roteamento por estado de enlace (Link State Routing Algorithm).

- A rede será composta por múltiplas subredes, cada uma contendo 2 hosts e 1 roteador (todos na mesma subrede).
- Os roteadores devem se conectar entre si em uma topologia aleatória (pelo menos parcialmente conectada).
- Cada roteador deve implementar o algoritmo de estado de enlace, mantendo uma base de dados dos enlaces (LSDB) e uma tabela de roteamento atualizada com base no algoritmo de Dijkstra.
- O processo em cada roteador deve envolver o uso de threads.
- Uso de um dos protocolos (TCP ou UDP) para a transmissão dos pacotes de controle da rede.

## 🔗 Topologia de Rede do Projeto
A presente topologia pode ser visualizada no network_graph.html do projeto

<img src="https://github.com/user-attachments/assets/e2ac310e-93bf-447c-aec7-cd71eaf98608" width="400">

## 🔗 Organização do Projeto
```
📁 NTW-Algorithm/
├── 📁 host/
│   ├── 🐳 Dockerfile
│   ├── 🐍 host.py
│   └── 📜 start.sh
│
├── 📁 lib/
│   ├── 📁 bindings/
│   ├── 📁 tom-select/
│   └── 📁 vis-9.1.2/
│
├── 📁 router/
│   ├── 🐍 dijkstra.py
│   ├── 🐳 Dockerfile
│   ├── 🐍 lsa.py
│   ├── 🐍 router.py
│   └── 📜 start.sh
│
├── 📁 script/
│   ├── 🐍 conexao_host.py
│   ├── 🐍 conexao_rt.py
│   ├── 🐍 graph_build.py
│   ├── 🐍 graph_demandas.py
│   ├── 🐍 graph_latencia.py
│   └── 🐍 mostrar_rt.py
│
├── 📄 .gitignore
├── 📝 comandos.txt
├── 🐳 docker-compose.yml
├── 🐍 gerar_grafo.py
├── 📜 LICENSE
├── 🌐 network_graph.html
└── 📦 requirements.txt
```

## 🔗 Ferramentas utilizadas
- Python
```
Python 3.12.6
```

- Docker
```
Docker version 28.0.4, build b8034c0
```

## 🔗 Como utilizar o algoritmo
1. Clone o repositório
```
git clone https://github.com/IagoraNz/NTW-Algorithm
```
2. Abra o projeto
```
cd NTW-Algorithm
```
3. Para obter a topologia visualizável em grafo no HTML (será necessário uma extensão para abrir o HTML, como o Live Server ou Five Server)
```
python3 gerar_grafo.py
```
5. Inicialize a topologia via Docker
```
docker compose up --build
```
4. Após uma certa quantidade de tempo, cheque a tabela de roteamento da rede
```
cd script
python3 mostrar_rt.py
```
5. Teste a conectividade dos roteadores
```
cd script
python3 conexao_rt.py
```
6. Teste a conectividade dos hosts
```
cd script
python3 conexao_host.py
```
7. Finalize a aplicação
```
docker compose down
```

## 🔗 Justificativa do Uso do Protocolo UDP
Justificativa do uso do protocolo UDP em uma topologia de rede com hosts e roteadores:

* **Baixa latência e simplicidade**:
  O UDP não realiza controle de conexão, verificação de entrega ou ordenação de pacotes, o que o torna mais leve e rápido. Isso é ideal para aplicações em tempo real, como transmissões multimídia, jogos online ou simulações de rede.

* **Redução de sobrecarga na rede**:
  Por dispensar mecanismos de confiabilidade presentes no TCP, o UDP gera menos tráfego e exige menos processamento dos roteadores e hosts, tornando-se mais eficiente em topologias com muitos nós.

* **Adequado para testes e simulações**:
  Sua simplicidade facilita o desenvolvimento de ambientes de teste e a análise de comportamento da rede sem interferências de protocolos mais complexos.

* **Maior flexibilidade para aplicações**:
  Como a confiabilidade pode ser tratada pela própria aplicação quando necessário, o uso do UDP permite maior controle sobre o comportamento da comunicação, adaptando-se melhor a diferentes cenários de rede.

## 🔗 Construção da topologia
A topologia da rede foi construída manualmente utilizando Docker Compose, com o objetivo de simular uma rede com múltiplas sub-redes interligadas por roteadores, onde cada sub-rede contém um roteador e dois hosts.

### ⚙️ Estrutura Geral
A rede é composta por 6 sub-redes (sn_1 a sn_6), cada uma com um intervalo de IP próprio (CIDR /24), conectadas entre si por roteadores que compartilham múltiplas interfaces de rede. Cada roteador está conectado:

- À sua sub-rede local (com seus hosts).

- A dois outros roteadores (topologia em anel).

Essa estrutura garante que a rede tenha redundância de caminhos e suporte ao protocolo de roteamento por estado de enlace.

### ⚙️ Componentes da Topologia

#### ROTEADORES

Cada roteador é configurado com:

- Um nome identificador (rtr_nome), IP principal (rtr_ip) e uma lista de vizinhos diretos com seus IPs e custos.

- Três interfaces de rede (uma por sub-rede):

  - Sua sub-rede local.

  - A sub-rede do roteador anterior.

  - A sub-rede do roteador seguinte.

#### HOSTS

Cada sub-rede possui dois hosts (por exemplo, host1_1 e host1_2), conectados exclusivamente à sua sub-rede e com o roteador local como gateway. Cada host é configurado com:

- IP fixo no intervalo .11 e .12.

- Variável de ambiente rtr_ip apontando para o IP do seu roteador.

- Dependência explícita do seu roteador (depends_on), garantindo que ele seja iniciado antes.

#### SUB-REDES
  
A definição das sub-redes (sn_1 a sn_6) foi feita manualmente com ipam (gerenciamento de IPs), garantindo controle total sobre os intervalos de endereçamento e evitando conflitos.
