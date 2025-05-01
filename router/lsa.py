import os
import json

RTR_IP = os.getenv("rtr_ip")
NGH = json.loads(os.getenv("vizinhanca"))

class LSA:
    @staticmethod
    def criar_pacote(sequencia: int):
        pacote = {
            "id": RTR_IP,
            "vizinhanca": NGH,
            "seq": sequencia
        }
        return pacote