#!/usr/bin/env python

###############################################################################
# Ferramenta: digita_texto.py
#
# Objetivo da ferramenta
# Automatizar a inserção de textos em aplicações que não possuem interface
# para importação de dados, simulando a digitação do conteúdo de um arquivo
# texto em uma janela selecionada pelo usuário através de um clique do mouse.
#
# Requisitos de execução
# - Python 3.8 ou superior.
# - Bibliotecas:
#     - pyautogui
#     - pygetwindow
#     - pynput
# - Permissão para controlar mouse e teclado no sistema operacional.
# - Arquivo texto contendo o conteúdo a ser digitado.
#
# Instalação das dependências:
#
#   pip install pyautogui pygetwindow pynput
#
# Forma de utilização
# 1. Crie um arquivo texto contendo as informações que serão digitadas.
# 2. Execute o script informando o arquivo como parâmetro:
#
#      python digita_texto.py texto.txt
#
# 3. Quando solicitado, clique na janela ou aplicação de destino.
# 4. O script irá:
#    - Identificar a janela selecionada.
#    - Trazer a janela para o primeiro plano.
#    - Simular a digitação do conteúdo do arquivo.
#
# Exemplos de uso
#
# Exemplo 1:
#
#   $ python digita_texto.py mensagem.txt
#
#   Clique na janela onde deseja digitar o texto...
#   Janela selecionada: Bloco de Notas
#
# Exemplo 2:
#
#   $ python digita_texto.py cadastro_cliente.txt
#
#   Clique na janela onde deseja digitar o texto...
#   Janela selecionada: Sistema ERP
#
# Casos de uso comuns:
#
# - Preenchimento automático de sistemas legados.
# - Inserção de informações em sessões RDP.
# - Automação de terminais SSH ou Telnet.
# - Alimentação de formulários sem API de integração.
# - Apoio a atividades operacionais repetitivas.
#
###############################################################################

import pyautogui
import pygetwindow as gw
from pynput import mouse
import time
import sys
import os

# === 1. Defina aqui o texto a ser digitado ===
if len(sys.argv) > 1:
    arquivo_texto = sys.argv[1]

    if not os.path.isfile(arquivo_texto):
        print(f"Arquivo não encontrado: {arquivo_texto}")
        sys.exit(1)

    with open(arquivo_texto, "r", encoding="utf-8") as f:
        texto_para_digitar = f.read()
else:
    print("Uso: python script.py <arquivo.txt>")
    sys.exit(1)

# === 2. Aguarda clique do mouse para selecionar a janela ===
def capturar_clique():
    print("Clique na janela onde deseja digitar o texto...")

    posicao = {}

    def on_click(x, y, button, pressed):
        if pressed:
            posicao['x'] = x
            posicao['y'] = y
            return False  # Encerra o listener

    with mouse.Listener(on_click=on_click) as listener:
        listener.join()

    return posicao['x'], posicao['y']

# === 3. Encontra e ativa a janela ===
def ativar_janela_por_posicao(x, y):
    for janela in gw.getAllWindows():
        if janela.left <= x <= janela.right and janela.top <= y <= janela.bottom:
            print(f"Janela selecionada: {janela.title}")
            janela.activate()
            time.sleep(1)
            return True
    return False

# === Execução ===
try:
    x, y = capturar_clique()
    if not ativar_janela_por_posicao(x, y):
        print("Nenhuma janela encontrada na posição clicada.")
        sys.exit(1)

    # === 4. Simula digitação ===
    pyautogui.write(texto_para_digitar, interval=0.01)

except Exception as e:
    print("Erro:", e)
