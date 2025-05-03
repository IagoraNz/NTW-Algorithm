import os
import threading
import time

CONT_CPU = os.cpu_count()
MAX = CONT_CPU * 4

def pegar_hosts():
    saida = os.popen("docker ps --filter 'name=host' --format '{{.Names}}'").read()
    return sorted(saida.splitlines())

def extrair_hosts(nome):
    prefixo = nome.split('-')[-2]
    res = prefixo.split('host')[-1]
    res1 = res[:-1].split('_')[0]
    res2 = res[-1]
    return res1, res2

def ping(de, para, ip, res, thread):
    ini = time.time()
    comando = f"docker exec {de} ping -c 1 -W 0.1 {ip} > /dev/null 2>&1"
    print(f"{comando}")
    codigo = os.system(comando)
    fim = time.time()
    tempo = fim - ini
    sucesso = (codigo == 0)
    
    with thread:
        res.append((de, para, sucesso, tempo))
        
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
        print(f"ROTEADOR {de}")
        for para, ok, tempo in sumario[de]:
            status = "SUCESSO" if ok else "FALHA"
            print(f"{de} --> {para}: {tempo:2f} [{status}]")
            total_ok += ok
            
    print(f"Conexoes que tiveram sucesso: {total_ok}/{total}")   