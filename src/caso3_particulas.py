from src.autor import Autor


class ResolvedorParticulas:

    def resolver(self, registros: list[Autor]) -> list[Autor]:
        if not registros:
            raise ValueError("Lista de registros não pode ser vazia")
        return list(registros)
