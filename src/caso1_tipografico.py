from collections import defaultdict

from src.autor import Autor
from src import normalizador


def _chave_tipografica(nome: str) -> str:
    sem_diacriticos = normalizador.remover_diacriticos(nome)
    sem_apostrofos = normalizador.normalizar_apostrofos(sem_diacriticos)
    return sem_apostrofos.lower().strip()


class ResolvedorTipografico:

    def resolver(self, registros: list[Autor]) -> list[Autor]:
        if not registros:
            raise ValueError("Lista de registros não pode ser vazia")

        grupos = self._agrupar_registros(registros)
        canonicos = self._resolver_canonicos(grupos)
        return self._mapear_para_canonicos(registros, canonicos)

    def _agrupar_registros(self, registros: list[Autor]) -> dict[str, list[str]]:
        grupos: dict[str, list[str]] = defaultdict(list)
        for registro in registros:
            grupos[_chave_tipografica(registro.nome)].append(registro.nome)
        return grupos

    def _resolver_canonicos(self, grupos: dict[str, list[str]]) -> dict[str, str]:
        canonicos = {}
        for chave, nomes in grupos.items():
            nome_canonico = normalizador.preferir_mais_acentuado(nomes)
            nome_canonico = normalizador.normalizar_apostrofos(nome_canonico)
            nome_canonico = normalizador.normalizar_unicode(nome_canonico)
            canonicos[chave] = nome_canonico
        return canonicos

    def _mapear_para_canonicos(self, registros: list[Autor], canonicos: dict[str, str]) -> list[Autor]:
        return [
            Autor(nome=canonicos[_chave_tipografica(r.nome)], id_autor=r.id_autor)
            for r in registros
        ]
