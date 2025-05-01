import os
import sys

def pegar_roteadores():
    saida = os.popen("docker ps --filter 'name=router' --format '{{.Names}}'").read()
    return sorted(saida.splitlines())

def pegar_tRoteamento(container):
    cmd = f"docker exec {container} ip route"
    print(f"{cmd}")
    return os.popen(cmd).read()

for container in pegar_roteadores():
    print(pegar_tRoteamento(container))