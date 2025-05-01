import json
import os
import socket
import threading
import time
import subprocess
import json
from typing import Dict, Tuple, Any

RTR_IP = os.getenv("rtr_ip")
RTR_NAME = os.getenv("rtr_nome")
NGH = json.loads(os.getenv("vizinhanca"))

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
        
        Log.log(f"Iniciando o roteador!")
        
    def enviar_pacotes(self) -> None:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sequencia = 0
        
        while True:
            pacote = {}
            try:
                pacote = {
                    "id": RTR_IP,
                    "vizinhanca": NGH,
                    "seq": sequencia
                }
                return pacote
            except Exception as error:
                Log.log(f"Não foi possível criar o pacote {e}")
                return {}
            
if __name__ == "__main__":
    r1 = Roteador()
    print(r1.enviar_pacotes())