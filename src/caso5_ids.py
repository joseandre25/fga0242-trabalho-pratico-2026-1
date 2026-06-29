from src.autor import Autor
from src.indice_ids_canonicos import IndiceIdsCanonicos


class ResolvedorIds:

    def resolver(self, registros: list[Autor]) -> list[Autor]:
        if not registros:
            raise ValueError("Lista de registros não pode ser vazia")

        indice = IndiceIdsCanonicos(registros)

        return [
            Autor(nome=registro.nome, id_autor=indice.id_de(registro.nome))
            for registro in registros
        ]
