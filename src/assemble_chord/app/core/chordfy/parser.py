import re


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