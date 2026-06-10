import pytest

from dados_loader import carregar_casos
from src.autor import Autor
from src.caso4_iniciais_agrupadas import ResolvedorIniciaisAgrupadas

_CENARIOS = carregar_casos("caso4.json")


class TestResolvedorIniciaisAgrupadas:
    
    

    def setup_method(self):
        self.resolvedor = ResolvedorIniciaisAgrupadas()


    @pytest.mark.caso4
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

    @pytest.mark.caso4
    def test_resolver_preserva_ids_originais(self):
        registros = [
            Autor(nome="Sérgio Henrique Guaraldi", id_autor="243350"),
            Autor(nome="SH Guaraldi", id_autor="954057"),
        ]


        resultado = self.resolvedor.resolver(registros)

        assert [a.id_autor for a in resultado] == ["243350", "954057"]


    @pytest.mark.caso4
    def test_resolver_preserva_quantidade_de_registros(self):
        registros = [
            Autor(nome="Vanilda Cristina Junior", id_autor="763027"),
            Autor(nome="VC Junior", id_autor="763027"),
        ]

        assert len(self.resolvedor.resolver(registros)) == 2

    @pytest.mark.caso4
    def test_resolver_compara_ignorando_acentos_no_sobrenome(self):
        registros = [
            Autor(nome="Vanilda Cristina Júnior", id_autor="763027"),
            Autor(nome="VC Junior", id_autor="763027"),
        ]

        resultado = self.resolvedor.resolver(registros)

        assert [a.nome for a in resultado] == [
            "Vanilda Cristina Júnior",
            "Vanilda Cristina Júnior",
        ]


    @pytest.mark.caso4
    def test_resolver_lista_vazia_lanca_excecao(self):
        with pytest.raises(ValueError):
            self.resolvedor.resolver([])
