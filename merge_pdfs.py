#!/usr/bin/env python3

###############################################################################
# Ferramenta: merge_pdfs.py
#
# Objetivo da ferramenta
# Unificar múltiplos arquivos PDF em um único documento, preservando a ordem
# dos arquivos informados durante a execução.
#
# Requisitos de execução
# - Python 3.8 ou superior.
# - Biblioteca PyPDF2 instalada.
# - Arquivos PDF válidos para processamento.
#
# Instalação da dependência:
#
#   pip install PyPDF2
#
# Forma de utilização
# 1. Execute o script informando os arquivos PDF de entrada.
# 2. Utilize a opção -o ou --output para definir o nome do arquivo final.
#
# Sintaxe:
#
#   python merge_pdfs.py arquivo1.pdf arquivo2.pdf arquivo3.pdf -o saida.pdf
#
# 3. O script irá:
#    - Ler os arquivos PDF informados.
#    - Unificar os documentos na ordem especificada.
#    - Gerar um único arquivo PDF de saída.
#
# Exemplos de uso
#
# Exemplo 1:
#
#   $ python merge_pdfs.py contrato.pdf anexo.pdf -o documento_final.pdf
#
# Saída:
#
#   Adicionando: contrato.pdf
#   Adicionando: anexo.pdf
#   PDF gerado com sucesso: documento_final.pdf
#
# Exemplo 2:
#
#   $ python merge_pdfs.py parte1.pdf parte2.pdf parte3.pdf -o completo.pdf
#
# Resultado:
#
#   Geração do arquivo completo.pdf contendo todos os documentos
#   informados na sequência especificada.
#
###############################################################################

import argparse
import os
import sys
from PyPDF2 import PdfMerger


def main():
    parser = argparse.ArgumentParser(
        description="Junta múltiplos arquivos PDF em um único documento."
    )

    parser.add_argument(
        "pdfs",
        nargs="+",
        help="Lista de arquivos PDF de entrada"
    )

    parser.add_argument(
        "-o",
        "--output",
        required=True,
        help="Nome do arquivo PDF de saída"
    )

    args = parser.parse_args()

    merger = PdfMerger()

    try:
        for pdf in args.pdfs:

            if not os.path.isfile(pdf):
                print(f"Erro: arquivo não encontrado: {pdf}")
                return 1

            if not pdf.lower().endswith(".pdf"):
                print(f"Erro: arquivo não é um PDF válido: {pdf}")
                return 1

            print(f"Adicionando: {pdf}")
            merger.append(pdf)

        merger.write(args.output)
        merger.close()

        print(f"\nPDF gerado com sucesso: {args.output}")
        print(f"Total de PDFs processados: {len(args.pdfs)}")

        return 0

    except Exception as e:
        print(f"Erro durante o processamento: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())