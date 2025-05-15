import time
import threading
import conexao_host
import matplotlib.pyplot as plt

REQUISICOES_FIXAS = [10, 50, 100]
ITERACOES = 50

resultados = {n_reqs: [] for n_reqs in REQUISICOES_FIXAS}

for n_reqs in REQUISICOES_FIXAS:
    print(f"Iniciando testes para {n_reqs} requisições simultâneas...")

    for iteracao in range(1, ITERACOES + 1):
        print(f"  Iteração {iteracao}/{ITERACOES}")

        res = []
        threads = []
        lock = threading.Lock()

        hosts = conexao_host.pegar_hosts()
        if len(hosts) < 2:
            print("Poucos hosts para testar!")
            break

        tarefas = []
        for _ in range(n_reqs):
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

        resultados[n_reqs].append((media_latencia, sucesso_pct))

# Gráficos
plt.figure(figsize=(12, 10))

cores = ['black', '#cfdcef', '#82c082']

# Latência média
plt.subplot(2, 1, 1)
for i, reqs in enumerate(REQUISICOES_FIXAS):
    latencias = [r[0] for r in resultados[reqs]]
    plt.plot(range(1, ITERACOES + 1), latencias, marker='o', label=f'{reqs} conexões', color=cores[i])
plt.title("Latência média ao longo das iterações")
plt.xlabel("Iterações")
plt.ylabel("Latência média (s)")
plt.legend()
plt.grid(True)

# Taxa de sucesso
plt.subplot(2, 1, 2)
for i, reqs in enumerate(REQUISICOES_FIXAS):
    sucessos = [r[1] for r in resultados[reqs]]
    plt.plot(range(1, ITERACOES + 1), sucessos, marker='x', label=f'{reqs} conexões', color=cores[i])
plt.title("Taxa de sucesso ao longo das iterações")
plt.xlabel("Iterações")
plt.ylabel("% Conexões bem-sucedidas")
plt.legend()
plt.grid(True)

plt.tight_layout()
plt.show()