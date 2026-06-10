import re
from collections import defaultdict

from src.autor import Autor
from src.normalizador import remover_diacriticos

_PARTICULAS = frozenset({"de", "da", "do", "das", "dos", "e"})


def _tokens(nome: str) -> list[str]:
    return re.findall(r"[^\W\d_]+", nome, flags=re.UNICODE)


def _normalizar(texto: str) -> str:
    return remover_diacriticos(texto).lower()


def _tokens_significativos(nome: str) -> list[str]:
    return [t for t in _tokens(nome) if _normalizar(t) not in _PARTICULAS]


def _eh_nome_completo(nome: str) -> bool:
    tokens = _tokens_significativos(nome)
    return len(tokens) >= 2 and all(len(t) > 1 for t in tokens)


def _assinatura(nome: str) -> tuple[str, ...]:
    tokens = _tokens_significativos(nome)
    return tuple(_normalizar(t)[0] for t in tokens)


def _preferir_nome(nomes: list[str]) -> str:
    completos = [n for n in nomes if _eh_nome_completo(n)]
    candidatos = completos if completos else nomes
    return max(candidatos, key=lambda n: len(_tokens(n)))


class ResolvedorParticulas:

    def resolver(self, registros: list[Autor]) -> list[Autor]:
        if not registros:
            raise ValueError("Lista de registros não pode ser vazia")

        grupos: dict[tuple[str, ...], list[str]] = defaultdict(list)
        for r in registros:
            grupos[_assinatura(r.nome)].append(r.nome)

        canonicos = {sig: _preferir_nome(nomes) for sig, nomes in grupos.items()}

        return [
            Autor(nome=canonicos[_assinatura(r.nome)], id_autor=r.id_autor)
            for r in registros
        ]
