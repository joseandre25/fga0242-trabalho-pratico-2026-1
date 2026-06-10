# Trabalho TPPE - Desduplicação de Autores

## Integrantes

- Esther Sena - 210162769
- José André - 211062016
- Erick Santos - 211061672
- Lucas Ribeiro - 211063185 
## Linguagem

Python

## Framework de Testes

[pytest](https://docs.pytest.org/) **8.1.1** (versão fixada em `requirements.txt`)

## Como executar

Instale as dependências:

```bash
pip install -r requirements.txt
```

Execute todos os testes:

```bash
pytest
```

Execute apenas os testes de um caso específico (categoria/marker, registrados em `pytest.ini`):

```bash
pytest -m caso1   # também: caso2, caso3, caso4, caso5, integracao
```

> A descoberta de testes está configurada em `pytest.ini` (`python_files = teste_*.py test_*.py`),
> pois os módulos de teste seguem o padrão `teste_*` (com "e"), diferente do padrão default do
> pytest (`test_*`). Sem essa configuração os testes não seriam coletados.

## Recursos do framework de testes utilizados

- **Suítes de teste**: cada caso possui seu próprio módulo em `tests/`, agrupando os cenários relacionados a uma mesma unidade.
- **Categorias de teste**: markers registrados em `pytest.ini` (`caso1`...`caso5`, `integracao`), permitindo filtrar a execução com `pytest -m <marker>`.
- **Testes parametrizados**: `@pytest.mark.parametrize`, alimentados pelos conjuntos de dados em `dados/*.json`, carregados via `tests/dados_loader.py::carregar_casos`.
- **Testes de exceção**: `pytest.raises`, para validar o comportamento das unidades diante de entradas inválidas.

## Estrutura do Projeto

```text
tppe-desduplicacao/
│
├── README.md
├── requirements.txt
├── pytest.ini
│
├── src/
│   ├── autor.py
│   ├── caso1_tipografico.py
│   ├── caso2_iniciais.py
│   ├── caso3_particulas.py
│   ├── caso4_iniciais_agrupadas.py
│   ├── caso5_ids.py
│   └── desduplicador.py
│
├── tests/
│   ├── dados_loader.py
│   ├── teste_caso1_tipografico.py
│   ├── teste_caso2_iniciais.py
│   ├── teste_caso3_particulas.py
│   ├── teste_caso4_iniciais_agrupadas.py
│   ├── teste_caso5_ids.py
│   └── teste_integracao.py
│
└── dados/
    ├── caso1.json
    ├── caso2.json
    ├── caso3.json
    ├── caso4.json
    └── caso5.json
```

## Convenção dos conjuntos de dados (`dados/*.json`)

Cada arquivo `dados/casoN.json` contém uma lista de cenários no formato:

```json
{
  "descricao": "explicação do cenário",
  "registros_originais": [{"id": "...", "nome": "..."}],
  "registros_esperados": [{"id": "...", "nome": "..."}]
}
```

`registros_originais` representa os dados de entrada (como recebidos de fontes diferentes) e
`registros_esperados` representa o resultado esperado após a deduplicação/curadoria, espelhando
as tabelas de antes/depois apresentadas no enunciado para cada caso. Use
`tests.dados_loader.carregar_casos("casoN.json")` para alimentar `@pytest.mark.parametrize`.

## Divisão Sugerida de Branches

| Branch | Responsável | Tarefa |
| --- | --- | --- |
| `feature/caso1` | Pessoa 1 | Diferenças de grafia |
| `feature/caso2` | Pessoa 2 | Sobrenome com iniciais |
| `feature/caso3` | Pessoa 3 | Partículas como `de`, `da`, `do`, `dos` |
| `feature/caso4` | Pessoa 4 | Iniciais agrupadas |
| `feature/caso5` | Pessoa 5 | Unificação de IDs |
| `feature/integracao` | Alguém | Testes de integração |

## Fluxo TDD

1. Criar a branch do caso.
2. Escrever os testes no arquivo correspondente em `tests/`.
3. Implementar a menor solução possível no arquivo correspondente em `src/`.
4. Rodar `pytest`.
5. Abrir Pull Request para revisão.
