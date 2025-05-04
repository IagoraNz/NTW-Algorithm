# ----------------------------------------------------------------------------------------------------------- #

'''
Bibliotecas necessárias
'''

import os

class Cores:
    LARANJA = '\033[38;2;224;167;106m'
    VERDE = '\033[38;2;66;191;161m'
    ROXO = '\033[38;2;161;114;243m'
    AZUL = '\033[38;2;114;186;243m'
    VERMELHO = '\033[38;2;243;138;138m'
    AMARELO = '\033[38;2;243;228;114m'
    SEM_COR = '\033[0m'

# ----------------------------------------------------------------------------------------------------------- #

'''
Funções principais
'''

def pegar_roteadores() -> list:
    """
    Pega os containers que estão rodando e filtra os que tem o nome 'router'.

    Returns:
        list: Lista com os nomes dos containers que tem o nome 'router'.
    """
    saida = os.popen("docker ps --filter 'name=router' --format '{{.Names}}'").read()
    return sorted(saida.splitlines())

def pegar_tRoteamento(container) -> str:
    """
    Executa o comando "ip route" no container especificado e retorna a saída.
    
    O comando "ip route" exibe a tabela de roteamento do container.

    Args:
        container (str): Nome do container.

    Returns:
        str: Saída do comando "ip route".
    """
    cmd = f"docker exec {container} ip route"
    print(f"{cmd}")
    return os.popen(cmd).read()

# ----------------------------------------------------------------------------------------------------------- #

'''
Execução do script
'''

for container in pegar_roteadores():
    print(pegar_tRoteamento(container))