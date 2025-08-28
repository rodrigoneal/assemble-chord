from src.assemble_chord.app.exceptions.chrods import FindChordError

CHROMATIC_NOTES = [
    ["C"],
    ["C#", "Db"],
    ["D"],
    ["D#", "Eb"],
    ["E"],
    ["F"],
    ["F#", "Gb"],
    ["G"],
    ["G#", "Ab"],
    ["A"],
    ["A#", "Bb"],
    ["B"],
]

NOTE_TO_INDEX = {note: i for i, names in enumerate(CHROMATIC_NOTES) for note in names}


def find_note_positions_on_string(open_note: str, target_note: str, frets: int):
    """
    Retorna em quais trastes de uma única corda a nota desejada aparece.

           Arguments:
                   open_note -- Nota da corda
                   target_note -- Nota a ser encontrada
                   frets -- Número de trastes a considerar

           Raises:
                   ValueError: Se a nota de afinação for inválida
                   ValueError: Se a nota alvo for inválida

           Returns:
                   list: Lista de trastes onde a nota alvo é encontrada
    """

    open_note = open_note.strip().capitalize()
    target_note = target_note.strip().capitalize()

    if open_note not in NOTE_TO_INDEX:
        raise FindChordError(f"Nota de afinação inválida: {open_note}")
    if target_note not in NOTE_TO_INDEX:
        raise FindChordError(f"Nota alvo inválida: {target_note}")

    open_index = NOTE_TO_INDEX[open_note]
    target_index = NOTE_TO_INDEX[target_note]

    trastes = []
    for fret in range(frets + 1):  # inclui a corda solta (traste 0)
        note_index = (open_index + fret) % 12
        if note_index == target_index:
            trastes.append(fret)

    return trastes
