import re

CAMPOS = {
    "C": ["C", "Dm", "Em", "F", "G", "Am", "Bdim"],
    "G": ["G", "Am", "Bm", "C", "D", "Em", "F#dim"],
    "D": ["D", "Em", "F#m", "G", "A", "Bm", "C#dim"],
    "A": ["A", "Bm", "C#m", "D", "E", "F#m", "G#dim"],
    "E": ["E", "F#m", "G#m", "A", "B", "C#m", "D#dim"],
    "B": ["B", "C#m", "D#m", "E", "F#", "G#m", "A#dim"],
    "F#": ["F#", "G#m", "A#m", "B", "C#", "D#m", "E#dim"],
    "C#": ["C#", "D#m", "E#m", "F#", "G#", "A#m", "B#dim"],
    "F": ["F", "Gm", "Am", "Bb", "C", "Dm", "Edim"],
    "Bb": ["Bb", "Cm", "Dm", "Eb", "F", "Gm", "Adim"],
    "Eb": ["Eb", "Fm", "Gm", "Ab", "Bb", "Cm", "Ddim"],
    "Ab": ["Ab", "Bbm", "Cm", "Db", "Eb", "Fm", "Gdim"],
    "Db": ["Db", "Ebm", "Fm", "Gb", "Ab", "Bbm", "Cdim"],
    "Gb": ["Gb", "Abm", "Bbm", "Cb", "Db", "Ebm", "Fdim"],
    "Cb": ["Cb", "Dbm", "Ebm", "Fb", "Gb", "Abm", "Bbdim"],
}

# Relativos menores
RELATIVOS = {k: v[5][:-1] if v[5].endswith("dim") else v[5] for k, v in CAMPOS.items()}

# Enarmonia
ENARMONICOS = {
    "Cb": "B",  # necessário para alguns casos raros
    "B#": "C",
    "Fb": "E",
    "E#": "F",
    # NOTA: Db, Eb, Ab, Gb permanecem iguais para não quebrar o campo harmônico
}

# Pesos por grau
PESOS = {
    0: 3,  # I
    1: 1,  # ii
    2: 1,  # iii
    3: 2,  # IV
    4: 3,  # V
    5: 1,  # vi
    6: 0.5,  # vii°
}


def parser_standard_chord_name(chord_str: str, bass: str | None = None) -> str:
    """Realiza as normalizações de notação PT -> EN

    Arguments:
            chord_str -- A string representando o acorde a ser normalizado.

    Keyword Arguments:
            bass -- A nota do baixo (default: {None})

    Returns:
            Uma string representando o acorde normalizado.
    """
    if not chord_str:
        return ""

    chord_str = chord_str.strip()

    # Remover barra de baixo, mas manter o baixo se necessário no final
    if bass:
        chord_str = chord_str.replace(f"/{bass}", "")

    chord_str = re.sub(r"^([A-G][b#]?)(?:7/4|74)$", r"\g<1>7sus4", chord_str)

    # Normalizações de notação PT -> EN
    replacements = {
        "7M": "maj7",  # 7M -> maj7
        "M7": "maj7",  # às vezes escrevem M7 em vez de 7M
        "7m": "m7",  # 7m -> m7
        "m7M": "mMaj7",  # menor com 7M
        "5+": "aug",  # 5+ -> aug
        "5-": "b5",  # 5- -> b5
        "º": "dim",
        "°": "dim",
        "ø": "m7b5",
        "(": "",
        ")": "",
        "/": "",
    }
    for old, new in replacements.items():
        chord_str = chord_str.replace(old, new)
    # Corrigir bemóis escritos como "b" no meio (caso A#b etc.)
    if len(chord_str) > 1 and chord_str[1] == "b":
        chord_str = chord_str[0] + "-" + chord_str[2:]  # music21 usa A- para Ab

    # Retornar acorde normalizado + baixo, se existir
    return chord_str


def simplify_chord(acorde: str) -> str:
    """
    Remove extensões (7, 9, maj7, 5-, sus, etc.) e retorna só a base normalizada.
    Exemplos:
      G#m7(5-) -> G#m
      F#m7M    -> F#
      C°       -> C
      E4       -> E
      Eb4(7/9) -> Eb
    """
    acorde = acorde.strip()

    # Reconhece diminutos
    if "°" in acorde or "dim" in acorde:
        base = re.match(r"([A-G][b#]?)(.*)", acorde).group(1)
        return ENARMONICOS.get(base, base) + "dim"

    # Reconhece meio-diminuto (m7b5, m7(5-), ø)
    if "7(5-)" in acorde or "m7b5" in acorde or "ø" in acorde:
        base = re.match(r"([A-G][b#]?)(.*)", acorde).group(1) + "m"
        return ENARMONICOS.get(base, base)

    # Reconhece maior com 7M / maj7
    if "7M" in acorde or "maj7" in acorde:
        base = re.match(r"([A-G][b#]?m?)(.*)", acorde).group(1)
        return ENARMONICOS.get(base, base)

    # Reconhece sus2 / sus4 e notas com extensão 4/2
    if "sus" in acorde or acorde.endswith("2") or acorde.endswith("4"):
        base = re.match(r"([A-G][b#]?)(.*)", acorde).group(1)
        return ENARMONICOS.get(base, base)

    # Caso geral: pega só a fundamental + m se for menor
    match = re.match(r"([A-G][b#]?m?)(.*)", acorde)
    if not match:
        return acorde
    base = match.group(1)
    return ENARMONICOS.get(base, base)


def parser_bemol(nota: str) -> str:
    """Normaliza bemóis para o padrão do music21."""
    if len(nota) > 1 and nota[1] == "b":
        return nota.replace("b", "-")
    return nota
