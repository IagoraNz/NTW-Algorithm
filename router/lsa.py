import os
import json

RTR_IP = os.getenv("rtr_ip")
NGH = json.loads(os.getenv("vizinhanca"))

class LSA:
    """
    Classe LSA (Link State Advertisement) representa um pacote de anúncio de estado de link.
    Contém informações sobre o roteador, sua vizinhança e a sequência do pacote.
    
    Attributes:
        sequencia (int): Sequência do pacote LSA.

    Returns:
        dict: Dicionário representando o pacote LSA.
    """
    @staticmethod
    def criar_pacote(sequencia: int):
        pacote = {
            "id": RTR_IP,
            "vizinhanca": NGH,
            "seq": sequencia
        }
        return pacote