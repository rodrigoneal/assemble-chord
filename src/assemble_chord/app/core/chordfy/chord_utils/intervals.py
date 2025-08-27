from dataclasses import dataclass


@dataclass
class Intervalo:
    indice: int
    nome: str

    INTERVAL_LABELS = {
        0: (1, ""),
        1: "2♭",
        2: "2ª",
        3: "3♭",
        4: "3ª",
        5: "4ª",
        6: "4♭",
        7: "5ª",
        8: "5♭",
        9: "6ª",
        10: "7♭",
        11: "7ª",
    }


class Intervalos:
    INTERVAL_LABELS = {
        0: (1, None),
        1: (2, "b"),
        2: (2, None),
        3: (3, "b"),
        4: (3, None),
        5: (4, None),
        6: (4, "b"),
        7: (5, None),
        8: (5, "b"),
        9: (6, None),
        10: (7, "b"),
        11: (7, None),
    }

    @classmethod
    def descricao(cls, intervalo: int) -> Intervalo | None:
        nome = cls.INTERVAL_LABELS.get(intervalo)
        if nome is None:
            return None
        return Intervalo(indice=intervalo, nome=nome)
