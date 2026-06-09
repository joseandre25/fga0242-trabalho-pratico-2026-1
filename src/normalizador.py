import unicodedata

_APOSTROFOS = frozenset({
    "`",  # ` GRAVE ACCENT (backtick)
    "‘",  # ' LEFT SINGLE QUOTATION MARK
    "’",  # ' RIGHT SINGLE QUOTATION MARK
    "‛",  # ‛ SINGLE HIGH-REVERSED-9 QUOTATION MARK
    "´",  # ´ ACUTE ACCENT
    "ʼ",  # ʼ MODIFIER LETTER APOSTROPHE
})
_APOSTROFO_CANONICO = "'"  # U+0027 APOSTROPHE


def normalizar_apostrofos(texto: str) -> str:
    return "".join(_APOSTROFO_CANONICO if c in _APOSTROFOS else c for c in texto)


def normalizar_unicode(texto: str) -> str:
    return unicodedata.normalize("NFC", texto)


def remover_diacriticos(texto: str) -> str:
    nfd = unicodedata.normalize("NFD", texto)
    return "".join(c for c in nfd if unicodedata.category(c) != "Mn")


def _contar_diacriticos(texto: str) -> int:
    nfd = unicodedata.normalize("NFD", texto)
    return sum(1 for c in nfd if unicodedata.category(c) == "Mn")


def preferir_mais_acentuado(nomes: list[str]) -> str:
    if not nomes:
        raise ValueError("Lista de nomes vazia")
    return max(nomes, key=lambda n: (_contar_diacriticos(n), len(n)))
