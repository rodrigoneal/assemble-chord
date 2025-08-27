import pytest

from src.assemble_chord.app.core.chordfy.notes import get_notes_from_chord


@pytest.mark.parametrize(
    "chord_str, bass, expected",
    [
        ("Absus4", None, ["Ab", "Db", "Eb"]),
        ("G7", None, ["G", "B", "D", "F"]),
        ("C/Bb", "Bb", ["C", "E", "G", "Bb"]),
        ("G/F", "F", ["G", "B", "D", "F"]),
        ("A7(#9)", None, ["A", "C#", "E", "G", "B#"]),
        ("A", None, ["A", "C#", "E"]),
        ("A7/C#", "C#", ["A", "C#", "E", "G"]),
        ("Amaj7", None, ["A", "C#", "E", "G#"]),
        ("A7/D", "D", ["A", "C#", "E", "G"]),
        ("Aadd9", None, ["A", "C#", "E", "B"]),
        ("B#7M", None, ["B#", "D#", "F#", "A#"]),
        ("G5+", None, ["G", "B", "D#"]),
        ("Bm7(5-)", None, ["B", "D", "F", "A"]),
        ("E7(b9)", None, ["E", "G#", "B", "D", "F"]),
        ("D7/4", None, ["D", "G", "A", "C"]),
        ("C/D", "D", ["C", "E", "G"]),
        ("Em7/5-", None, ["E", "G", "Bb", "D"]),
        ("D#°", None, ["D#", "F#", "A"]),
    ],
)
def test_parse_chord_with_extensions(chord_str, bass, expected):
    result = get_notes_from_chord(chord_str)
    assert result.all_notes == expected
    assert result.bass == bass
