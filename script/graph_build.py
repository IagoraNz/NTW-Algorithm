import time
import os
import statistics
import matplotlib.pyplot as plt

NUM_EXECUCOES = 50
TEMPOS = []

for i in range(1, NUM_EXECUCOES + 1):
    print(f"[{i}/{NUM_EXECUCOES}] Executando: docker compose build...")
    inicio = time.time()
    codigo = os.system("docker compose build > /dev/null 2>&1")  # ou use --no-cache se quiser
    fim = time.time()
    duracao = fim - inicio
    TEMPOS.append(duracao)

# Estatísticas
media = statistics.mean(TEMPOS)
minimo = min(TEMPOS)
maximo = max(TEMPOS)

# Plot do gráfico
plt.figure(figsize=(10, 5))
plt.plot(range(1, NUM_EXECUCOES + 1), TEMPOS, marker='o', linestyle='-', color='black', label='Tempo de build')
plt.axhline(media, color='green', linestyle='--', label=f'Média ({media:.2f}s)')
plt.title("Tempo de execução do 'docker compose build'")
plt.xlabel("Execução")
plt.ylabel("Tempo (s)")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()