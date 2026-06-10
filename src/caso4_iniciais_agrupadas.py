import re

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


def _assinatura_nome_completo(nome: str) -> tuple[str, str]:
    tokens = _tokens_significativos(nome)
    iniciais_agrupadas = "".join(_normalizar(t)[0] for t in tokens[:-1])
    sobrenome = _normalizar(tokens[-1])
    return iniciais_agrupadas, sobrenome


def _assinatura_abreviada(nome: str) -> tuple[str, str] | None:
    tokens = _tokens(nome)
    if len(tokens) != 2:
        return None

    iniciais_agrupadas, sobrenome = tokens
    if len(iniciais_agrupadas) < 2:
        return None

    return _normalizar(iniciais_agrupadas), _normalizar(sobrenome)


class ResolvedorIniciaisAgrupadas:

    def resolver(self, registros: list[Autor]) -> list[Autor]:
        if not registros:
            raise ValueError("Lista de registros não pode ser vazia")

        nomes_completos = {
            _assinatura_nome_completo(r.nome): r.nome
            for r in registros
            if _eh_nome_completo(r.nome)
        }

        resolvidos = []
        for registro in registros:
            assinatura = _assinatura_abreviada(registro.nome)
            nome = nomes_completos.get(assinatura, registro.nome)
            resolvidos.append(Autor(nome=nome, id_autor=registro.id_autor))

        return resolvidos
