from src.autor import Autor
from src import normalizador


class ResolvedorTipografico:

    def resolver(self, registros: list[Autor]) -> list[Autor]:
        if not registros:
            raise ValueError("Lista de registros não pode ser vazia")
        nomes = [r.nome for r in registros]
        nome_canonico = normalizador.preferir_mais_acentuado(nomes)
        nome_canonico = normalizador.normalizar_apostrofos(nome_canonico)
        nome_canonico = normalizador.normalizar_unicode(nome_canonico)
        return [Autor(nome=nome_canonico, id_autor=r.id_autor) for r in registros]
