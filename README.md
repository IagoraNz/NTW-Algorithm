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
