# ----------------------------------------------------------------------------------------------------------- #

'''
Bibliotecas necessárias e variáveis globais
'''

import os
import threading
import time

class Cores:
    LARANJA = '\033[38;2;224;167;106m'
    VERDE = '\033[38;2;66;191;161m'
    ROXO = '\033[38;2;161;114;243m'
    AZUL = '\033[38;2;114;186;243m'
    VERMELHO = '\033[38;2;243;138;138m'
    AMARELO = '\033[38;2;243;228;114m'
    SEM_COR = '\033[0m'

CONT_CPU = os.cpu_count()
MAX = CONT_CPU * 4

# ----------------------------------------------------------------------------------------------------------- #

'''
Funções principais
'''

def pegar_hosts() -> list:
    """
    Pega os containers que estão rodando e filtra os que tem o nome 'host'.
    Retorna uma lista com os nomes dos containers.

    Returns:
        list: Lista com os nomes dos containers que tem o nome 'host'.
    """
    saida = os.popen("docker ps --filter 'name=host' --format '{{.Names}}'").read()
    return sorted(saida.splitlines())

def extrair_hosts(nome) -> tuple:
    """
    Extrai o prefixo e o sufixo do nome do container cujo nome começa com 'host'.
    
    Se o nome do container não estiver no formato esperado, retorna None.

    Args:
        nome (str): Nome do container.

    Returns:
        tuple: Tupla com o prefixo e o sufixo do nome do container.
    """
    prefixo = nome.split('-')[-2]
    res = prefixo.split('host')[-1]
    res1 = res[:-1].split('_')[0]
    res2 = res[-1]
    return res1, res2

def ping(de, para, ip, res, thread) -> None:
    """
    Executa o comando ping no container de origem (de) para o container de destino (para).
    O resultado é armazenado na lista res. O tempo de execução é medido e armazenado na lista res.

    Args:
        de (str): Nome do container de origem.
        para (str): Nome do container de destino.
        ip (str): IP do container de destino.
        res (list): Lista onde o resultado será armazenado.
        thread (threading.Lock): Lock para garantir acesso seguro à lista res.
    """
    ini = time.time()
    comando = f"docker exec {de} ping -c 1 -W 0.1 {ip} > /dev/null 2>&1"
    print(f"{comando}")
    codigo = os.system(comando)
    fim = time.time()
    tempo = fim - ini
    sucesso = (codigo == 0)
    
    with thread:
        res.append((de, para, sucesso, tempo))
        
# ----------------------------------------------------------------------------------------------------------- #
 
'''
Execução do script
'''
        
if __name__ == "__main__":
    hosts = pegar_hosts()
    if not hosts:
        print(f"[ERRO] Execute docker compose up --build primeiro!")
        exit(1)
        
    tarefas = [(de, para, f"172.20.{extrair_hosts(para)[0]}.1{extrair_hosts(para)[1]}") for de in hosts for para in hosts if de != para]
    
    res = []
    threads = []
    thread_lock = threading.Lock()
    
    for de, para, ip in tarefas:
        while len(threads) >= MAX:
            threads = [t for t in threads if t.is_alive()]
            
        thread = threading.Thread(target=ping, args=(de, para, ip, res, thread_lock))
        thread.start()
        threads.append(thread)
        
    for thread in threads:
        thread.join()
        
    sumario = {}
    for de, para, ok, tempo in res:
        sumario.setdefault(de, []).append((de, ok, tempo))
        
    total_ok = 0
    total = len(res)
    
    for de in sorted(sumario):
        print(f"HOST {de}")
        for para, ok, tempo in sumario[de]:
            status = "SUCESSO" if ok else "FALHA"
            print(f"{de} --> {para}: {tempo:2f} [{status}]")
            total_ok += ok
            
    print(f"Conexoes que tiveram sucesso: {total_ok}/{total}")