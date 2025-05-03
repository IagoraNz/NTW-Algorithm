import os
import threading
import time

CONT_CPU = os.cpu_count()
MAX = CONT_CPU * 4

def pegar_roteadores():
    saida = os.popen("docker ps --filter 'name=router' --format '{{.Names}}'").read()
    return sorted(saida.splitlines())

def extrair_roteadores(nome):
    prefixo = nome.split('-')[-2]
    res = prefixo.split('router')[1]
    return res

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
    roteadores = pegar_roteadores()
    if not roteadores:
        print(f"[ERRO] Execute docker compose up --build primeiro!")
        exit(1)
    
    tarefas = [(f, t, f"172.20.{extrair_roteadores(t)}.3") for f in roteadores for t in roteadores if f != t]
    
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