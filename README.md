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

