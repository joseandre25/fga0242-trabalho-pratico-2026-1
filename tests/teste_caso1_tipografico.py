import pytest
from src.autor import Autor
from src.caso1_tipografico import ResolvedorTipografico
from dados_loader import carregar_casos

_CENARIOS = carregar_casos("caso1.json")


class TestNormalizadorUtilidades:
    """Suíte de testes para os utilitários de normalização de caracteres (src/normalizador.py).

    Esses utilitários são propostos para Caso 1 mas podem ser reutilizados pelos demais casos.
    """

    @pytest.mark.caso1
    @pytest.mark.parametrize("entrada,esperado", [
        ("Sant`anna", "Sant'anna"),       # ` GRAVE ACCENT → '
        ("Sant’anna", "Sant'anna"),  # ’ RIGHT SINGLE QUOTATION MARK → '
        ("Sant‘anna", "Sant'anna"),  # ‘ LEFT SINGLE QUOTATION MARK → '
        ("Sant'anna", "Sant'anna"),       # já correto, permanece inalterado
    ])
    def test_normaliza_apostrofos(self, entrada, esperado):
        from src.normalizador import normalizar_apostrofos
        assert normalizar_apostrofos(entrada) == esperado

    @pytest.mark.caso1
    @pytest.mark.parametrize("entrada,esperado", [
        ("Sérgio", "Sergio"),
        ("Mônica", "Monica"),
        ("Gonçalves", "Goncalves"),
        ("Luiz", "Luiz"),
    ])
    def test_remove_diacriticos(self, entrada, esperado):
        from src.normalizador import remover_diacriticos
        assert remover_diacriticos(entrada) == esperado

    @pytest.mark.caso1
    @pytest.mark.parametrize("nomes,esperado", [
        (["Sergio", "Sérgio"], "Sérgio"),
        (["Monica", "Mônica"], "Mônica"),
        (["Sérgio", "Sergio"], "Sérgio"),
        (["Luiz", "Luiz"], "Luiz"),
    ])
    def test_prefere_nome_mais_acentuado(self, nomes, esperado):
        from src.normalizador import preferir_mais_acentuado
        assert preferir_mais_acentuado(nomes) == esperado

    @pytest.mark.caso1
    def test_preferir_mais_acentuado_lista_vazia_lanca_excecao(self):
        from src.normalizador import preferir_mais_acentuado
        with pytest.raises(ValueError):
            preferir_mais_acentuado([])


class TestResolvedorTipografico:
    """Suíte de testes para o Caso 1 — diferenças tipográficas/grafia."""

    def setup_method(self):
        self.resolvedor = ResolvedorTipografico()

    @pytest.mark.caso1
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

    @pytest.mark.caso1
    def test_resolver_preserva_ids_originais(self):
        registros = [
            Autor(nome="Sergio Henrique Guaraldi", id_autor="554799"),
            Autor(nome="Sérgio Henrique Guaraldi", id_autor="243350"),
        ]
        resultado = self.resolvedor.resolver(registros)
        assert [a.id_autor for a in resultado] == ["554799", "243350"]

    @pytest.mark.caso1
    def test_resolver_preserva_quantidade_de_registros(self):
        registros = [
            Autor(nome="Sergio", id_autor="100"),
            Autor(nome="Sérgio", id_autor="200"),
        ]
        assert len(self.resolvedor.resolver(registros)) == 2

    @pytest.mark.caso1
    def test_resolver_nome_ja_canonico_permanece_inalterado(self):
        registros = [Autor(nome="Mônica Hirata Sant'anna", id_autor="31299")]
        resultado = self.resolvedor.resolver(registros)
        assert resultado[0].nome == "Mônica Hirata Sant'anna"

    @pytest.mark.caso1
    def test_resolver_lista_vazia_lanca_excecao(self):
        with pytest.raises(ValueError):
            self.resolvedor.resolver([])
