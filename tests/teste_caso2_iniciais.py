import pytest
from dados_loader import carregar_casos
from src.autor import Autor
from src.caso2_iniciais import ResolvedorIniciais

_CENARIOS = carregar_casos("caso2.json")


class TestResolvedorIniciais:
    
    
    def setup_method(self):
        self.resolvedor = ResolvedorIniciais()

    @pytest.mark.caso2
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
        nomes_esperados = [r["nome"] for r in cenario["registros_esperados"]]

        resultado = self.resolvedor.resolver(registros)

        assert [a.nome for a in resultado] == nomes_esperados

    @pytest.mark.caso2
    def test_resolver_preserva_ids_originais(self):
        registros = [
            Autor(nome="Ana de Mattos Seabra", id_autor="28372"),
            Autor(nome="Seabra A M", id_autor="582585"),
        ]

        resultado = self.resolvedor.resolver(registros)

        assert [a.id_autor for a in resultado] == ["28372", "582585"]

    @pytest.mark.caso2
    def test_resolver_preserva_quantidade_de_registros(self):
        registros = [
            Autor(nome="Cassius de Souza", id_autor="28371"),
            Autor(nome="Souza C.", id_autor="746936"),
        ]

        assert len(self.resolvedor.resolver(registros)) == 2

    @pytest.mark.caso2
    def test_resolver_compara_ignorando_acentos_nas_iniciais(self):
        registros = [
            Autor(nome="Cássio de Souza", id_autor="28371"),
            Autor(nome="Souza C.", id_autor="746936"),
        ]

        resultado = self.resolvedor.resolver(registros)

        assert [a.nome for a in resultado] == ["Cássio de Souza", "Cássio de Souza"]

    @pytest.mark.caso2
    def test_resolver_lista_vazia_lanca_excecao(self):
        with pytest.raises(ValueError):
            self.resolvedor.resolver([])
