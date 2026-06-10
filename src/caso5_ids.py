from src.autor import Autor
from src.normalizador import remover_diacriticos


def _chave_nome(nome: str) -> str:
    return remover_diacriticos(nome).lower().strip()


def _menor_id(ids: list[str]) -> str:
    return min(ids, key=int)


class ResolvedorIds:

    def resolver(self, registros: list[Autor]) -> list[Autor]:
        if not registros:
            raise ValueError("Lista de registros não pode ser vazia")

        ids_por_chave: dict[str, list[str]] = {}
        for registro in registros:
            chave = _chave_nome(registro.nome)
            ids_por_chave.setdefault(chave, []).append(registro.id_autor)

        id_canonico = {chave: _menor_id(ids) for chave, ids in ids_por_chave.items()}

        return [
            Autor(nome=registro.nome, id_autor=id_canonico[_chave_nome(registro.nome)])
            for registro in registros
        ]
