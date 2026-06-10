import pytest

from dados_loader import carregar_casos
from src.autor import Autor
from src.caso5_ids import ResolvedorIds

_CENARIOS = carregar_casos("caso5.json")


class TestResolvedorIds:
    """Suíte de testes para o Caso 5 — unificação de IDs para o mesmo autor."""

    def setup_method(self):
        self.resolvedor = ResolvedorIds()

    @pytest.mark.caso5
    @pytest.mark.parametrize(
        "cenario",
        _CENARIOS,
        ids=[c["descricao"] for c in _CENARIOS],
    )
    def test_resolver_por_cenario(self, cenario):
        registros = [
            Autor(nome=r["nome"], id_autor=r["id"])
            for r in cenario["registros_originais"]
        ]
        esperados = cenario["registros_esperados"]

        resultado = self.resolvedor.resolver(registros)

        assert [a.nome for a in resultado] == [r["nome"] for r in esperados]
        assert [a.id_autor for a in resultado] == [r["id"] for r in esperados]

    @pytest.mark.caso5
    def test_resolver_preserva_nomes_originais(self):
        registros = [
            Autor(nome="Raphael Goncalves Viana", id_autor="433094"),
            Autor(nome="Raphael Gonçalves Viana", id_autor="31298"),
        ]

        resultado = self.resolvedor.resolver(registros)

        assert [a.nome for a in resultado] == [
            "Raphael Goncalves Viana",
            "Raphael Gonçalves Viana",
        ]

    @pytest.mark.caso5
    def test_resolver_preserva_quantidade_de_registros(self):
        registros = [
            Autor(nome="Yuri Vieira Faria", id_autor="713900"),
            Autor(nome="Yuri Vieira Faria", id_autor="31300"),
        ]

        assert len(self.resolvedor.resolver(registros)) == 2

    @pytest.mark.caso5
    def test_resolver_agrupa_ignorando_acentos(self):
        registros = [
            Autor(nome="Raphael Goncalves Viana", id_autor="433094"),
            Autor(nome="Raphael Gonçalves Viana", id_autor="31298"),
        ]

        resultado = self.resolvedor.resolver(registros)

        assert [a.id_autor for a in resultado] == ["31298", "31298"]

    @pytest.mark.caso5
    def test_resolver_nao_altera_autores_distintos(self):
        registros = [
            Autor(nome="Ana Silva", id_autor="100"),
            Autor(nome="Bruno Costa", id_autor="200"),
        ]

        resultado = self.resolvedor.resolver(registros)

        assert [a.id_autor for a in resultado] == ["100", "200"]

    @pytest.mark.caso5
    def test_resolver_lista_vazia_lanca_excecao(self):
        with pytest.raises(ValueError):
            self.resolvedor.resolver([])
