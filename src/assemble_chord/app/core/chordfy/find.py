from music21 import interval, pitch

from src.assemble_chord.app.exceptions.chrods import FindChordError


def normalize_note(note: str) -> str:
    """
    Normaliza entrada para formato aceito pelo music21.
    """
    return note.strip().capitalize()


def find_note_on_string(open_note: str, fret: int) -> list[str]:
    """
    Retorna a nota (com enarmonias) pressionada em uma corda afinada em `open_note`
    na casa `fret`.

    Exemplo:
        find_note_on_string("D", 5) -> ["G"]
        find_note_on_string("E", 1) -> ["F", "E#"]
    """
    try:
        open_pitch = pitch.Pitch(normalize_note(open_note))
    except Exception:
        raise FindChordError(f"Corda {open_note} não reconhecida.")

    # cada casa equivale a 1 semitom
    pressed_note = open_pitch.transpose(fret)

    # pega enarmonia
    enharmonic = pressed_note.getEnharmonic()

    if pressed_note.name != enharmonic.name:
        return [pressed_note.name, enharmonic.name]
    return [pressed_note.name]


def find_note_positions_on_string(
    open_note: str, target_note: str, frets: int
) -> list[int]:
    """
    Retorna em quais trastes de uma corda a nota desejada aparece.
    """
    try:
        open_pitch = pitch.Pitch(normalize_note(open_note))
        target_pitch = pitch.Pitch(normalize_note(target_note))
    except Exception:
        raise FindChordError(f"Nota inválida: {open_note} ou {target_note}")

    trastes = []
    for fret in range(frets + 1):  # inclui a corda solta
        pressed_note = open_pitch.transpose(fret)

        # compara por classe de altura (independente de enarmonia)
        if pressed_note.pitchClass == target_pitch.pitchClass:
            trastes.append(fret)
    if not trastes:
        raise FindChordError(f"Nota {target_note} não encontrada na corda {open_note}.")

    return trastes
