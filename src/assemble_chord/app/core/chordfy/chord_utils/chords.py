class Acordes:
    EXTENSIONS = {
        "9": 14,
        "11": 17,
        "13": 21,
    }

    QUALITY_ALIASES = {
        "7M": "maj7",
        "M7": "maj7",
        "m7b5": "m7(5-)",
        "ø": "m7(5-)",
    }

    @classmethod
    def traduz_qualidade(cls, simbolo: str) -> str:
        """Retorna o alias da qualidade ou o próprio símbolo se não existir."""
        return cls.QUALITY_ALIASES.get(simbolo, simbolo)

    @classmethod
    def in_(cls, simbolo: str) -> bool:
        """Verifica se o símbolo está nos aliases de qualidade."""
        return simbolo in cls.QUALITY_ALIASES
