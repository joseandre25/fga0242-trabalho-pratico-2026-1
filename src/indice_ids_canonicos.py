from src.autor import Autor
from src.normalizador import remover_diacriticos


class IndiceIdsCanonicos:
    """Mapeia cada autor ao seu ID canônico — o menor ID dentre os registros homônimos."""

    def __init__(self, registros: list[Autor]) -> None:
        ids_por_chave: dict[str, list[str]] = {}
        for registro in registros:
            chave = self._chave_nome(registro.nome)
            ids_por_chave.setdefault(chave, []).append(registro.id_autor)

        self._id_canonico = {
            chave: self._menor_id(ids) for chave, ids in ids_por_chave.items()
        }

    def id_de(self, nome: str) -> str:
        return self._id_canonico[self._chave_nome(nome)]

    @staticmethod
    def _chave_nome(nome: str) -> str:
        return remover_diacriticos(nome).lower().strip()

    @staticmethod
    def _menor_id(ids: list[str]) -> str:
        return min(ids, key=int)
