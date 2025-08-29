import re

note_map = {
    "a": 0,
    "b": 1,
    "c": 2,
    "d": 3,
    "e": 4,
    "f": 5,
    "g": 6,
    "h": 7,
    "i": 8,
    "j": 9,
    "k": 10,
    "l": 11,
    "m": 12,
    "n": 13,
    "o": 14,
    "p": 15,
    "q": 16,
    "r": 17,
    "s": 18,
    "t": 19,
    "u": 20,
    "v": 21,
    "w": 22,
    "x": "x",
    "$": 4,
    "#": 8,
}


def remove_duplicates(lst):
    seen = set()
    result = []
    for item in lst:
        t = tuple(item)
        if t not in seen:
            seen.add(t)
            result.append(item)
    return result


def decode_chords(raw, instrument="cavaco") -> list[list[int]]:
    """Decodifica os acordes de uma string bruta do site Banana.

    Arguments:
            raw -- String bruta dos acordes

    Keyword Arguments:
            instrument -- Instrumento a ser utilizado (default: {"cavaco"})

    Returns:
            Descrição do retorno
    """
    simplified = re.sub(r"@(.).{4}.", r"\1", raw)
    chords = simplified.split(" ")
    result = []

    if instrument == "cavaco":
        for chord_str in chords:
            chord = []
            b = float("inf")  # menor traste
            e = float("-inf")  # maior traste
            f = 0
            for g in range(2, 6):  # cavaquinho usa 4 cordas
                if g >= len(chord_str):
                    continue
                h = note_map.get(chord_str[g], "x")
                if h != "x":
                    h = int(h) + 2 if g == 5 else int(h)  # ajuste da última corda
                    b = min(b, h)
                    e = max(e, h)
                    f += 1
                chord.append(h)
            # só pega acordes válidos
            if e < 17 and e - b < 6 and f >= 3:
                result.append(chord)
        result = remove_duplicates(result)
    else:
        for chord_str in chords:
            chord = [note_map.get(ch, "x") for ch in chord_str]
            result.append(chord)
    return result
