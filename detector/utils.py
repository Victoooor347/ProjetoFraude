# detector/utils.py

import csv

def processar_csv(caminho_arquivo):
    with open(caminho_arquivo, newline='', encoding='utf-8') as arquivo_csv:
        leitor = csv.DictReader(arquivo_csv)
        for linha in leitor:
            print(linha)  # aqui você coloca sua lógica real
