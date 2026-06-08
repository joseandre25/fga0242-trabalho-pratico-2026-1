import json
from pathlib import Path

DIRETORIO_DADOS = Path(__file__).resolve().parent.parent / "dados"


def carregar_casos(nome_arquivo):
    caminho = DIRETORIO_DADOS / nome_arquivo
    with caminho.open(encoding="utf-8") as arquivo:
        return json.load(arquivo)
