import re

from music21 import chord, harmony, interval, note

from src.assemble_chord.app.core.entity.chord import ChordEntity, Note


def get_quality(chord_str: str) -> str | None:
    match = re.match(r"^([A-G][#b]?)(.*)$", chord_str)
    if not match:
        return None
    quality = match.group(2)
    return quality if quality else None


def standard_chord_name(chord_str: str, bass: str | None = None) -> str:
    """
    Normaliza o nome de acordes escritos em português para o padrão do music21.
    Ex: C7M -> Cmaj7, F#m(5-) -> F#m(b5), G7(9) -> G9, Ab/Db -> Ab/Db
    """
    if not chord_str:
        return ""

    chord_str = chord_str.strip()

    # Remover barra de baixo, mas manter o baixo se necessário no final
    if bass:
        chord_str = chord_str.replace(f"/{bass}", "")

    chord_str = re.sub(r"^([A-G][b#]?)(?:7/4|74)$", r"\g<1>7sus4", chord_str)

    # Remover parênteses e barras internas
    chord_str = chord_str.replace("(", "").replace(")", "").replace("/", "")

    # Normalizações de notação PT -> EN
    replacements = {
        "7M": "maj7",  # 7M -> maj7
        "M7": "maj7",  # às vezes escrevem M7 em vez de 7M
        "7m": "m7",  # 7m -> m7
        "m7M": "mMaj7",  # menor com 7M
        "5+": "aug",  # 5+ -> aug
        "5-": "b5",  # 5- -> b5
        "sus4": "sus4",  # já está ok, mas garantimos
        "sus2": "sus2",
        "add9": "add9",
        "9": "9",  # nona já é padrão
        "11": "11",
        "13": "13",
        "º": "dim",
        "°": "dim",
        "ø": "m7b5",
    }
    for old, new in replacements.items():
        chord_str = chord_str.replace(old, new)

    # Se vier "ø" (meio diminuto), normalizar para m7b5
    if "ø" in chord_str:
        chord_str = chord_str.replace("ø", "m7b5")

    # Se o acorde começa com nota + "b" (ex: "Bb"), music21 entende.
    # Mas se vier como "Bb7M", já normalizamos acima para Bbmaj7.

    # Corrigir bemóis escritos como "b" no meio (caso A#b etc.)
    if len(chord_str) > 1 and chord_str[1] == "b":
        chord_str = chord_str[0] + "-" + chord_str[2:]  # music21 usa A- para Ab

    # Retornar acorde normalizado + baixo, se existir
    return chord_str


def get_bass(chord_str: str) -> str | None:
    match = re.match(r"^([A-G][#b]?[^(/]*)(?:/([A-G][#b]?))$", chord_str)
    if not match:
        return None
    return match.group(2)


INTERVAL_TYPES_PT = {
    "P": "justo",
    "M": "maior",
    "m": "menor",
    "A": "aumentado",
    "d": "diminuto",
}


def is_seventh_of_root(root_note: str, candidate_note: str) -> bool:
    """
    Verifica se candidate_note é a 7ª (maior ou menor) de root_note.
    Retorna 'M7', 'm7' ou None.
    """
    root_note = root_note + "3"
    candidate_note = candidate_note + "4"
    root = note.Note(root_note)
    candidate = note.Note(candidate_note)
    iv = interval.Interval(root, candidate)
    if (iv.generic.value % 7 == 0) and "m" in iv.name:
        return True
    return False


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

    try:
        h = harmony.ChordSymbol(chord_name)
    except Exception as e:
        raise ValueError(f"Acorde inválido: {chord_name}") from e
    root = h.root()
    c = chord.Chord(h.pitches)
    if is_seventh_of_root(root_note=root.name, candidate_note=bass) if bass else False:
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


def parse_chord_with_extensions(chord_str) -> ChordEntity:
    """
    Parser completo de acordes modernos, incluindo:
    - sus2, sus4
    - b5, #5
    - extensões 6,9,11,13
    - slash chords (A/B)
    Retorna (root, {nota: função})
    """
    # Detecta slash chord fora dos parênteses
    bass = get_bass(chord_str)

    # Regex para root, qualidade e extensões
    match = re.match(r"([A-G][b#]?)([^\(]*)(\(([^)]+)\))?", chord_str)
    if not match:
        raise ValueError(f"Acorde inválido: {chord_str}")

    _chord_name = standard_chord_name(chord_str, bass)

    notes = get_chord_notes_full(_chord_name, bass)
    quality = get_quality(_chord_name)

    root = [n.name for n in notes if n.is_root][0]

    return ChordEntity(
        notes=notes, root=root, chord=chord_str, quality=quality, bass=bass
    )  # valida com pydantic


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

    open_note: nota da corda solta (ex: "D")
    target_note: nota a buscar (ex: "F#" ou "Gb")
    frets: número de trastes a considerar

    Retorna: lista de trastes [0, 4, 16...]
    """
    open_note = open_note.strip().capitalize()
    target_note = target_note.strip().capitalize()

    if open_note not in NOTE_TO_INDEX:
        raise ValueError(f"Nota de afinação inválida: {open_note}")
    if target_note not in NOTE_TO_INDEX:
        raise ValueError(f"Nota alvo inválida: {target_note}")

    open_index = NOTE_TO_INDEX[open_note]
    target_index = NOTE_TO_INDEX[target_note]

    trastes = []
    for fret in range(frets + 1):  # inclui a corda solta (traste 0)
        note_index = (open_index + fret) % 12
        if note_index == target_index:
            trastes.append(fret)

    return trastes
