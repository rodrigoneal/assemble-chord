import re

from music21 import interval, note


def is_seventh_of_root(root_note: str, candidate_note: str) -> bool:
    """
    Verifica se candidate_note é a 7ª (menor) de root_note.

    Arguments:
            root_note -- C
            candidate_note -- B

    Returns:
            True se candidate_note é a 7ª menor de root_note, False caso contrário.
    """
    root_note = root_note + "3"
    candidate_note = candidate_note + "4"
    root = note.Note(root_note)
    candidate = note.Note(candidate_note)
    iv = interval.Interval(root, candidate)
    if (
        (iv.generic.value % 7 == 0) and "m" in iv.name
    ):  # As vezes a oitava é a mesma e vai gerar 14 tons de diferença, então pegamos o resto da divisão e verificamos se é divisível por 7 e o nome do intervalo contém "m"(menor)
        return True
    return False


def get_bass(chord_str: str) -> str | None:
    """Retorna a nota do baixo de um acorde.

    Arguments:
            chord_str -- A representação em string do acorde.

    Returns:
            A nota do baixo do acorde ou None se não for encontrado.
    """
    match = re.match(r"^([A-G][#b]?[^(/]*)(?:/([A-G][#b]?))$", chord_str)
    if not match:
        return None
    return match.group(2)


def get_extensions(chord_str: str) -> str | None:
    """Retorna as extensões de um acorde.

    Arguments:
            chord_str -- A representação em string do acorde.

    Returns:
            As extensões do acorde ou None se não forem encontradas.
    """
    match = re.match(r"^([A-G][#b]?)(.*)$", chord_str)
    if not match:
        return None
    extensions = match.group(2)
    return extensions if extensions else None
