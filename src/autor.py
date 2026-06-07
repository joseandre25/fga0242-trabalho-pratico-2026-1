from dataclasses import dataclass


@dataclass
class Autor:
    nome: str
    id_autor: str | None = None
