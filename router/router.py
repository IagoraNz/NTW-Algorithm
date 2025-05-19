# ----------------------------------------------------------------------------------------------------------- #

'''
Bibliotecas necessárias e variáveis globais
'''

import json
import os
import time
import threading
import socket
import subprocess
from typing import Dict, Tuple, Any
from dijkstra import dijkstra
from lsa import LSA

RTR_IP = os.getenv("rtr_ip")
RTR_NAME = os.getenv("rtr_nome")
NGH = json.loads(os.getenv("vizinhanca"))
PORTA_LSA = 5000

# ----------------------------------------------------------------------------------------------------------- #

class Configuracoes:
    """
    Classe Configuracoes, responsável por gerenciar as rotas do roteador.

    Returns:
        None
    """
    @staticmethod
    def obter_rotas(rotas: Dict[str, str]) -> Tuple[Dict[str, str], Dict[str, str], Dict[str, str]]:
        """
        Obtém todas as rotas existentes no sistema e compara com as novas rotas.
        
        Args:
            rotas: Dicionário com as novas rotas a serem configuradas (destino -> próximo_salto)
        
        Returns:
            Dicionário com as novas rotas a serem adicionadas
            Dicionário com as rotas a serem removidas
            Dicionário com as rotas a serem substituídas
        """
        rotas_existentes = {}
        rotas_sistema = {}
        adicionar = {}
        substituir = {}
        
        try:
            novas_rotas = {}
            for destino, proximo_salto in rotas.items():
                parts = destino.split('.')
                prefixo = '.'.join(parts[:3])
                network = f"{prefixo}.0/24"
                novas_rotas[network] = proximo_salto
            
            resultado = subprocess.run(
                ["ip", "route", "show"],
                capture_output=True,
                text=True,
                check=True
            )
            
            for linha in resultado.stdout.splitlines():
                partes = linha.split()
                
                if partes[0] != "default" and partes[1] == "via":
                    rede = partes[0]  # ex: 172.20.5.0/24
                    proximo_salto = partes[2]  # ex: 172.20.4.3
                    rotas_existentes[rede] = proximo_salto
                    
                elif partes[1] == 'dev':
                    rede = partes[0]
                    proximo_salto = partes[-1]
                    rotas_sistema[rede] = proximo_salto
                
            # Replace rotas que mudaram
            for rede, proximo_salto in novas_rotas.items():
                if (rede in rotas_existentes) and (rotas_existentes[rede] != proximo_salto):
                    substituir[rede] = proximo_salto
                    
            # Adicionar rotas inexistentes
            for rede, proximo_salto in novas_rotas.items():
                if (rede not in rotas_existentes) and (rede not in rotas_sistema):
                    adicionar[rede] = proximo_salto

            return adicionar, substituir    
        except Exception as e:
            Log.log(f"Erro ao obter rotas existentes: {e}")
            return {}, {}
        
    @staticmethod
    def add_rotas(salto: str, destino: str) -> bool:
        """
        Adiciona uma rota ao sistema.

        Args:
            salto (str): Próximo salto
            destino (str): Destino da rota

        Returns:
            bool: True se a rota foi adicionada com sucesso, False caso contrário.
        """
        try:
            p = destino.split('.')
            prefixo = '.'.join(p[:3])
            destino = f"{prefixo}.0/24"
            
            comando = f"ip route add {destino} via {salto}"
            processo = subprocess.run(
                comando.split(),
                capture_output=True
            )
            Log.log(f"[LOG] Rota adicionada com sucesso!")
        except subprocess.CalledProcessError as error:
            Log.log(f"[ERROR] Erro ao adicionar rota: {error}")
        except Exception as e:
            Log.log(f"[ERROR] Erro ao tentar adicionar rota: {error}")
    
    @staticmethod
    def subst_rotas(salto: str, destino: str) -> bool:
        """
        Substitui uma rota existente no sistema.
        
        Args:
            salto (str): Próximo salto
            destino (str): Destino da rota

        Returns:
            bool: True se a rota foi substituída com sucesso, False caso contrário.
        """
        try:
            p = destino.split('.')
            prefixo = '.'.join(p[:3])
            destino = f"{prefixo}.0/24"
            
            comando = f"ip route replace {destino} via {salto}"
            processo = subprocess.run(comando.split(), check=True)
            Log.log(f"[LOG] Rota substituída: {destino} via {salto}") if processo.returncode == 0 else Log.log(f"[LOG] Problema ao substituir rota: {processo.stderr.decode()}")
            return True
        except Exception as error:
            Log.log(f"[LOG] Erro de substituicao de rotas: {error}")
        return False
    
    @staticmethod
    def configurar_inter(lsdb: Dict[str, Any]) -> None:
        """
        Configura as rotas do roteador com base na LSDB (Link State Database) recebida.
        A função utiliza o algoritmo de Dijkstra para calcular os caminhos mais curtos e
        atualiza as rotas do sistema.

        Args:
            lsdb (Dict[str, Any]): Dicionário que representa a LSDB (Link State Database).
                Cada chave é o ID do roteador e o valor é um dicionário com informações sobre o roteador,
                incluindo a vizinhança.
        """
        rotas = dijkstra(RTR_IP, lsdb)
        
        caminhos = {}
        for destino, salto in rotas.items():
            for v, ip_custo in NGH.items():
                ip, _ = ip_custo
                if salto == ip:
                    caminhos[destino] = salto
                    break
                
        add, substituir = Configuracoes.obter_rotas(caminhos)
        for destino, salto in add.items():
            Configuracoes.add_rotas(salto, destino)
                
        for destino, salto in substituir.items():
            Configuracoes.subst_rotas(salto, destino)

class Log:
    """
    Classe Log, responsável por registrar mensagens de log com timestamp.
    Contém métodos para registrar mensagens de log.
    """
    @staticmethod
    def log(msg: str) -> None:
        """
        Registra uma mensagem de log com timestamp.
        O timestamp é formatado como "YYYY-MM-DD HH:MM:SS".

        Args:
            msg (str): Mensagem a ser registrada no log.
        """
        timestmp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        print(f"[{RTR_IP}] {msg} - {timestmp}", flush=True)

class Roteador:
    """
    Classe Roteador, responsável por gerenciar a comunicação entre os roteadores.
    """
    def __init__(self) -> None:
        """
        Inicializa a classe Roteador, criando um dicionário para armazenar a LSDB (Link State Database)
        e um lock para garantir acesso seguro à LSDB durante operações de leitura e escrita.
        """
        self.lsdb = {}
        self.thread = threading.Lock()
        
        Log.log(f"Iniciando o roteador!")
        
    def enviar_pacotes(self) -> None:
        """
        Envia pacotes LSA (Link State Advertisement) para os vizinhos a cada 10 segundos.
        O pacote contém informações sobre o roteador, sua vizinhança e a sequência do pacote.
        """
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
                Log.log(f"[{ip}] A mensagem foi enviado com sucesso!")
                
            with self.thread:
                self.lsdb[RTR_IP] = pacote
                self.salvar_lsdb(self.lsdb)
                Configuracoes.configurar_inter(self.lsdb)
                
            time.sleep(10)
            
    def receber_pacotes(self) -> None:
        """
        Recebe pacotes LSA (Link State Advertisement) de outros roteadores.
        Se o pacote recebido for mais recente do que o armazenado, atualiza a LSDB (Link State Database)
        e reenvia o pacote para os vizinhos.
        """
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        try:
            sock.bind(("0.0.0.0", PORTA_LSA))
        except socket.error as bind_error:
            return

        while True:
            try:
                dado, end = sock.recvfrom(4096)
                Log.log(f"Pacote recebido de {end}")
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
                        Configuracoes.configurar_inter(self.lsdb)
                
                Log.log(f"Recebendo pacote dessa origem: {origem}")
            except socket.error as error:
                Log.log(f"Erro ao receber LSA: {error}")
            except json.JSONDecodeError:
                Log.log("Erro ao decodificar LSA recebido.")
            except Exception as error:
                Log.log(f"Erro inesperado ao receber LSA: {error}")
          
    def salvar_lsdb(self, lsdb: Dict[str, Any]) -> None:
        """
        Salva a LSDB (Link State Database) em um arquivo JSON.
        O arquivo é salvo com o nome "lsdb.json" e contém as informações sobre os roteadores e suas vizinhanças.

        Args:
            lsdb (Dict[str, Any]): Dicionário que representa a LSDB (Link State Database).
                Cada chave é o ID do roteador e o valor é um dicionário com informações sobre o roteador,
                incluindo a vizinhança.
        """
        try:
            with open("lsdb.json", "w") as file:
                json.dump(lsdb, file, indent=4)
        except Exception as error:
            Log.log(f"[{error}] Erro ao salvar o LSDB")
               
# ----------------------------------------------------------------------------------------------------------- #

'''
Execução do roteador
'''               

if __name__ == "__main__":
    r1 = Roteador()
    
    threads = [
        threading.Thread(target=r1.enviar_pacotes, daemon=True, name="enviar_lsa"),
        threading.Thread(target=r1.receber_pacotes, daemon=True, name="receber_lsa"),
    ]
    
    for thread in threads:
        thread.start()
    threading.Event().wait()