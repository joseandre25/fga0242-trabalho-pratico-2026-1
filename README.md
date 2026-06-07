# Trabalho TPPE - Desduplicação de Autores

## Integrantes

- Esther - 210162769
- Nome - Matrícula
- Nome - Matrícula

## Linguagem

Python

## Framework de Testes

pytest

## Como executar

Instale as dependências:

```bash
pip install -r requirements.txt
```

Execute os testes:

```bash
pytest
```

## Estrutura do Projeto

```text
tppe-desduplicacao/
│
├── README.md
├── requirements.txt
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
