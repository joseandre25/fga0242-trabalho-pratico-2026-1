from src.autor import Autor
from src.caso1_tipografico import ResolvedorTipografico
from src.caso2_iniciais import ResolvedorIniciais
from src.caso3_particulas import ResolvedorParticulas
from src.caso4_iniciais_agrupadas import ResolvedorIniciaisAgrupadas
from src.caso5_ids import ResolvedorIds


class Desduplicador:

    def __init__(self) -> None:
        self._resolvedores = [
            ResolvedorTipografico(),
            ResolvedorIniciais(),
            ResolvedorParticulas(),
            ResolvedorIniciaisAgrupadas(),
            ResolvedorIds(),
        ]

    def desduplicar(self, registros: list[Autor]) -> list[Autor]:
        if not registros:
            raise ValueError("Lista de registros não pode ser vazia")

        resultado = registros
        for resolvedor in self._resolvedores:
            resultado = resolvedor.resolver(resultado)
        return resultado
