import json
import os
import socket
import threading
import time
import subprocess
import json
from typing import Dict, Tuple, Any
from lsa import LSA

RTR_IP = os.getenv("rtr_ip")
RTR_NAME = os.getenv("rtr_nome")
NGH = json.loads(os.getenv("vizinhanca"))
PORTA_LSA = 5000

print(NGH)

class Log:
    @staticmethod
    def log(msg: str) -> None:
        timestmp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        print(f"[{RTR_IP}] {msg} - {timestmp}", flush=True)

class Roteador:
    def __init__(self) -> None:
        self.lsdb = {}
        self.thread = threading.Lock()
        
        # Log.log(f"Iniciando o roteador!")
        
    def enviar_pacotes(self) -> None:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sequencia = 0
        
        while True:
            sequencia += 1
            pacote = LSA.criar_pacote(sequencia)
        
            msg = json.dumps(pacote).encode()
            for v, ip_custo in NGH.items():
                ip, custo = ip_custo
            
                sock.sendto(msg, (ip, PORTA_LSA))
                # Log.log(f"[{ip}] A mensagem foi enviado com sucesso!")
                
            with self.thread:
                self.lsdb[RTR_IP] = pacote
                self.salvar_lsdb(self.lsdb)
                
            time.sleep(10)
            
    def receber_pacotes(self) -> None:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        try:
            sock.bind(("0.0.0.0", PORTA_LSA))
        except socket.error as bind_error:
            return

        while True:
            try:
                dado, end = sock.recvfrom(4096)
                # Log.log(f"Pacote recebido de {end}")
                lsa = json.loads(dado.decode())
                origem = lsa["id"]
                
                if origem not in self.lsdb or lsa["seq"] > self.lsdb[origem]["seq"]:
                    for v, ip_custo in NGH.items():
                        ip, _ = ip_custo
                        if ip != end[0]:
                            sock.sendto(dado, (ip, PORTA_LSA))
                
                    with self.thread:
                        self.lsdb[origem] = lsa
                        self.salvar_lsdb(self.lsdb)
                
                # Log.log(f"Recebendo pacote dessa origem: {origem}")
            except socket.error as error:
                Log.log(f"Erro ao receber LSA: {error}")
            except json.JSONDecodeError:
                Log.log("Erro ao decodificar LSA recebido.")
            except Exception as error:
                Log.log(f"Erro inesperado ao receber LSA: {error}")
          
    def salvar_lsdb(self, lsdb: Dict[str, Any]):
        try:
            with open("lsdb.json", "w") as file:
                json.dump(lsdb, file, indent=4)
        except Exception as error:
            Log.log(f"[{error}] Erro ao salvar o LSDB")
               
if __name__ == "__main__":
    r1 = Roteador()
    
    threads = [
        threading.Thread(target=r1.enviar_pacotes, daemon=True, name="enviar_lsa"),
        threading.Thread(target=r1.receber_pacotes, daemon=True, name="receber_lsa"),
    ]
    
    for thread in threads:
        thread.start()
    threading.Event().wait()