import pytest
from dados_loader import carregar_casos
from src.autor import Autor
from src.caso3_particulas import ResolvedorParticulas

_CENARIOS = carregar_casos("caso3.json")


class TestResolvedorParticulas:

    def setup_method(self):
        self.resolvedor = ResolvedorParticulas()

    @pytest.mark.caso3
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

    @pytest.mark.caso3
    def test_resolver_preserva_ids_originais(self):
        registros = [
            Autor(nome="Luiz de Oliveira de Souza", id_autor="746937"),
            Autor(nome="Luiz Oliveira Souza", id_autor="608296"),
            Autor(nome="Luiz de O. de Souza", id_autor="549242"),
        ]

        resultado = self.resolvedor.resolver(registros)

        assert [a.id_autor for a in resultado] == ["746937", "608296", "549242"]

    @pytest.mark.caso3
    def test_resolver_preserva_quantidade_de_registros(self):
        registros = [
            Autor(nome="Luiz de Oliveira de Souza", id_autor="746937"),
            Autor(nome="Luiz Oliveira Souza", id_autor="608296"),
        ]

        assert len(self.resolvedor.resolver(registros)) == 2

    @pytest.mark.caso3
    def test_resolver_nome_sem_particula_unifica_para_forma_com_particula(self):
        registros = [
            Autor(nome="Maria de Souza de Lima", id_autor="611001"),
            Autor(nome="Maria Souza Lima", id_autor="611002"),
        ]

        resultado = self.resolvedor.resolver(registros)

        assert [a.nome for a in resultado] == [
            "Maria de Souza de Lima",
            "Maria de Souza de Lima",
        ]

    @pytest.mark.caso3
    def test_resolver_abreviacao_com_ponto_unifica_para_forma_completa(self):
        registros = [
            Autor(nome="Maria de Souza de Lima", id_autor="611001"),
            Autor(nome="Maria de S. de Lima", id_autor="611003"),
        ]

        resultado = self.resolvedor.resolver(registros)

        assert [a.nome for a in resultado] == [
            "Maria de Souza de Lima",
            "Maria de Souza de Lima",
        ]

    @pytest.mark.caso3
    def test_resolver_nome_ja_completo_permanece_inalterado(self):
        registros = [Autor(nome="Luiz de Oliveira de Souza", id_autor="746937")]

        resultado = self.resolvedor.resolver(registros)

        assert resultado[0].nome == "Luiz de Oliveira de Souza"

    @pytest.mark.caso3
    def test_resolver_lista_vazia_lanca_excecao(self):
        with pytest.raises(ValueError):
            self.resolvedor.resolver([])
