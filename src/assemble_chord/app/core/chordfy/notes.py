from music21 import chord, harmony, interval

from src.assemble_chord.app.core.chordfy import util
from src.assemble_chord.app.core.chordfy.parser import parser_standard_chord_name
from src.assemble_chord.app.core.entity.chord import ChordEntity, Note


def get_chord_notes_full(chord_name: str, bass: str | None = None):
    """
    Retorna lista de dicionários para cada nota do acorde:
    {
        'nota': 'C4',
        'grau': 1, 3, 5, 7, 9, ...
        'acidente': '#', 'b', ou None
        'tipo': 'maior', 'menor', 'justo', 'aumentado', 'diminuto'
    }
    """
    INTERVAL_TYPES_PT = {
        "P": "justo",
        "M": "maior",
        "m": "menor",
        "A": "aumentado",
        "d": "diminuto",
    }

    try:
        h = harmony.ChordSymbol(chord_name)
    except Exception as e:
        raise ValueError(f"Acorde inválido: {chord_name}") from e
    root = h.root()
    c = chord.Chord(h.pitches)
    if (
        util.is_seventh_of_root(root_note=root.name, candidate_note=bass)
        if bass
        else False
    ):
        chord_notes = [note for note in h.pitches]
        root_octave = root.octave
        c = chord.Chord(chord_notes + [bass + f"{root_octave + 1}"])
    notes_info = []

    for p in c.pitches:
        iv = interval.Interval(noteStart=root, noteEnd=p)
        # Grau diatônico simples
        degree_base = (iv.generic.directed - 1) % 7 + 1
        octave_add = (iv.generic.directed - 1) // 7
        degree = degree_base + 7 * octave_add  # Ajusta para 9, 11, 13...

        # Tipo do intervalo
        quality_code = iv.simpleName[0] if iv.simpleName else None
        tipo = INTERVAL_TYPES_PT.get(quality_code, None)

        # Detecta acidente
        accident = None
        nota = p.nameWithOctave
        accident = None
        if "#" in nota:
            accident = "#"
        elif "b" in nota or "-" in nota:
            accident = "b"

        note = Note(
            name=nota, degree=degree, note_accidental=accident, degree_accidental=tipo
        )
        notes_info.append(note)

    return notes_info


def get_notes_from_chord(chord_str) -> ChordEntity:
    """Retorna as notas de um acorde a partir de sua representação em string.

    Arguments:
        chord_str -- A string representando o acorde a ser analisado.

    Raises:
        ValueError: Se o acorde for inválido.

    Returns:
        ChordEntity: Um objeto contendo informações sobre o acorde.
    """
    bass = util.get_bass(chord_str)
    _chord_name = parser_standard_chord_name(chord_str, bass)
    notes = get_chord_notes_full(_chord_name, bass)
    extensions = util.get_extensions(_chord_name)
    root = [n.name for n in notes if n.is_root][0]
    return ChordEntity(
        notes=notes, root=root, chord=chord_str, extensions=extensions, bass=bass
    )  # valida com pydantic
