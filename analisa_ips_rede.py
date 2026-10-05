#!/usr/bin/env python3

###############################################################################
# Ferramenta: analisa_ips_rede.py
#
# Objetivo da ferramenta
# Analisar uma lista de endereços IP, identificar lacunas na sequência
# numérica e verificar, através de testes de conectividade (ping), quais
# endereços IP ausentes estão disponíveis para utilização na rede.
#
# Requisitos de execução
# - Sistema operacional Linux, Unix ou Windows.
# - Python 3 instalado.
# - Permissão para execução do comando ping.
# - Arquivo texto contendo um IP por linha.
#
# Forma de utilização
# 1. Crie um arquivo texto contendo os IPs utilizados na rede.
# 2. Execute o script informando o arquivo como parâmetro:
#
#      python analisa_ips_rede.py arquivo_ips.txt
#
# 3. O script irá:
#    - Carregar e ordenar os IPs informados.
#    - Identificar IPs faltantes na sequência.
#    - Testar a conectividade dos IPs ausentes.
#    - Exibir quais IPs estão livres ou em uso.
#    - Gerar o arquivo ips_disponiveis.txt contendo os IPs disponíveis.
#
# Exemplos de uso
#
# Conteúdo do arquivo ips.txt:
#
#   192.168.1.1
#   192.168.1.2
#   192.168.1.5
#   192.168.1.10
#
# Execução:
#
#   $ python analisa_ips_rede.py ips.txt
#
# Saída:
#
#   Carregando IPs do arquivo: ips.txt
#   Total de IPs no arquivo: 4
#   Total de IPs faltantes encontrados: 6
#
#   [1/6] Testando 192.168.1.3... ❌ LIVRE
#   [2/6] Testando 192.168.1.4... ✅ Em uso
#   ...
#
#   RESULTADO FINAL
#   IPs LIVRES encontrados : 3
#
# Arquivo gerado:
#
#   ips_disponiveis.txt
#
# Contendo a lista dos IPs identificados como disponíveis.
#
###############################################################################

import sys
import subprocess
import ipaddress
from typing import List


def load_ips(file_path: str) -> List[str]:
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            ips = [line.strip() for line in f if line.strip()]
        return sorted(ips, key=ipaddress.ip_address)
    except FileNotFoundError:
        print(f"Erro: Arquivo '{file_path}' não encontrado.")
        sys.exit(1)
    except Exception as e:
        print(f"Erro ao ler o arquivo: {e}")
        sys.exit(1)


def find_missing_ips(ips: List[str]) -> List[str]:
    """Retorna a lista de IPs que estão faltando na sequência."""
    if len(ips) < 2:
        return []
    
    missing = []
    try:
        ip_objs = [ipaddress.ip_address(ip) for ip in ips]
        
        for i in range(len(ip_objs) - 1):
            current = ip_objs[i]
            next_ip = ip_objs[i + 1]
            
            if int(next_ip) - int(current) > 1:
                gap_start = int(current) + 1
                gap_end = int(next_ip) - 1
                for m in range(gap_start, gap_end + 1):
                    missing.append(str(ipaddress.ip_address(m)))
    except ValueError as e:
        print(f"Erro: IP inválido detectado: {e}")
        sys.exit(1)
    
    return missing


def is_ip_alive(ip: str, timeout: int = 2) -> bool:
    """Testa se o IP responde a ping."""
    try:
        param = '-n' if sys.platform.startswith('win') else '-c'
        command = ['ping', '-c', '1', '-W', str(timeout), ip]
        
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=timeout + 2)
        return result.returncode == 0
    except:
        return False


def main():
    if len(sys.argv) < 2:
        print("Uso: python analisa_ips_rede.py <arquivo_ips.txt>")
        sys.exit(1)

    file_path = sys.argv[1]
    
    print(f"Carregando IPs do arquivo: {file_path}\n")
    ips = load_ips(file_path)
    
    if not ips:
        print("Nenhum IP encontrado no arquivo.")
        sys.exit(0)

    print(f"Total de IPs no arquivo: {len(ips)}\n")
    
    # Encontra os IPs faltantes
    missing_ips = find_missing_ips(ips)
    
    if not missing_ips:
        print("Nenhum IP faltando na sequência. A lista está completa!")
        sys.exit(0)
    
    print(f"Total de IPs faltantes encontrados: {len(missing_ips)}\n")
    print("Testando apenas os IPs faltantes...\n")
    
    free_ips = []
    
    for i, ip in enumerate(missing_ips, 1):
        print(f"[{i:3d}/{len(missing_ips)}] Testando {ip}...", end=" ")
        if is_ip_alive(ip):
            print("✅ Em uso")
        else:
            print("❌ LIVRE")
            free_ips.append(ip)

    # Resultado Final
    print("\n" + "="*60)
    print("RESULTADO FINAL")
    print("="*60)
    print(f"IPs testados (faltantes)    : {len(missing_ips)}")
    print(f"IPs LIVRES encontrados      : {len(free_ips)}")
    
    if free_ips:
        print("\nIPs DISPONÍVEIS:")
        for ip in free_ips:
            print(f"   • {ip}")
        
        # Salva em arquivo
        with open("ips_disponiveis.txt", "w", encoding="utf-8") as f:
            f.write("\n".join(free_ips))
        print(f"\nLista salva em: ips_disponiveis.txt")
    else:
        print("\nTodos os IPs faltantes estão em uso.")


if __name__ == "__main__":
    main()
