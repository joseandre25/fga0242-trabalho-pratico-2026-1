import pytest

from dados_loader import carregar_casos
from src.autor import Autor
from src.desduplicador import Desduplicador

_CENARIOS = carregar_casos("integracao.json")


class TestDesduplicadorIntegracao:
    """Suíte de testes de integração do pipeline completo de desduplicação."""

    def setup_method(self):
        self.desduplicador = Desduplicador()

    @pytest.mark.integracao
    @pytest.mark.parametrize(
        "cenario",
        _CENARIOS,
        ids=[c["descricao"] for c in _CENARIOS],
    )
    def test_desduplicar_por_cenario(self, cenario):
        registros = [
            Autor(nome=r["nome"], id_autor=r["id"])
            for r in cenario["registros_originais"]
        ]
        esperados = cenario["registros_esperados"]

        resultado = self.desduplicador.desduplicar(registros)

        assert [a.nome for a in resultado] == [r["nome"] for r in esperados]
        assert [a.id_autor for a in resultado] == [r["id"] for r in esperados]

    @pytest.mark.integracao
    def test_desduplicar_preserva_quantidade_de_registros(self):
        registros = [
            Autor(nome="Sergio Henrique Guaraldi", id_autor="554799"),
            Autor(nome="Sérgio Henrique Guaraldi", id_autor="243350"),
            Autor(nome="SH Guaraldi", id_autor="954057"),
        ]

        assert len(self.desduplicador.desduplicar(registros)) == 3

    @pytest.mark.integracao
    def test_desduplicar_lista_vazia_lanca_excecao(self):
        with pytest.raises(ValueError):
            self.desduplicador.desduplicar([])
