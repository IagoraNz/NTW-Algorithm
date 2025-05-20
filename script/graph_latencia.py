# ----------------------------------------------------------------------------------------------------------- #

'''
Bibliotecas necessárias e variáveis globais
'''

import time
import threading
import conexao_host
import matplotlib.pyplot as plt

MAX_TESTES = 20  # Número crescente de conexões simultâneas por rodada
resultados = []

# ----------------------------------------------------------------------------------------------------------- #

for n_conexoes in range(1, MAX_TESTES + 1):
    print(f"Testando com {n_conexoes} conexões simultâneas...")

    res = []
    threads = []
    lock = threading.Lock()

    hosts = conexao_host.pegar_hosts()
    if len(hosts) < 2:
        print("Poucos hosts para testar!")
        break

    tarefas = []
    for _ in range(n_conexoes):
        de = hosts[0]
        para = hosts[1]
        ip = f"172.20.{conexao_host.extrair_hosts(para)[0]}.1{conexao_host.extrair_hosts(para)[1]}"
        tarefas.append((de, para, ip))

    inicio = time.time()
    for de, para, ip in tarefas:
        t = threading.Thread(target=conexao_host.ping, args=(de, para, ip, res, lock))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()
    fim = time.time()

    tempo_total = fim - inicio
    sucesso_total = sum(1 for _, _, ok, _ in res if ok)
    latencias = [tempo for _, _, ok, tempo in res if ok]

    media_latencia = sum(latencias) / len(latencias) if latencias else 0
    sucesso_pct = (sucesso_total / len(res)) * 100 if res else 0

    resultados.append((n_conexoes, tempo_total, media_latencia, sucesso_pct))

# Plot
conexoes = [r[0] for r in resultados]
tempos_totais = [r[1] for r in resultados]
latencias_medias = [r[2] for r in resultados]
sucessos = [r[3] for r in resultados]

plt.figure(figsize=(8, 12))

plt.subplot(2, 1, 1)
plt.plot(conexoes, latencias_medias, marker='o', color='black', label="Latência média (s)")
plt.xlabel("Conexões simultâneas")
plt.ylabel("Latência (s)")
plt.title("Latência média vs. Conexões")
plt.grid(True)

plt.subplot(2, 1, 2)
plt.plot(conexoes, sucessos, marker='x', color='green', label="% Sucesso")
plt.xlabel("Conexões simultâneas")
plt.ylabel("% Conexões bem-sucedidas")
plt.title("Taxa de sucesso vs. Conexões")
plt.grid(True)

plt.tight_layout()
plt.show()