import pytest

from src.assemble_chord.app.core.chordfy.find import find_note_positions_on_string
from src.assemble_chord.app.exceptions.chrods import FindChordError


@pytest.mark.parametrize(
    "open_note, target_note, frets, expected",
    [
        ("D", "E", 12, [2]),
        ("A", "C", 12, [3]),
        ("E", "G", 12, [3]),
        ("G", "G", 12, [0, 12]),
    ],
)
def test_se_encontra_nota_no_braco_do_cavaco(open_note, target_note, frets, expected):
    positions = find_note_positions_on_string(open_note, target_note, frets)
    assert positions == expected


def test_se_nao_encontra_nota_no_braco_do_cavaco():
    with pytest.raises(FindChordError):
        find_note_positions_on_string("B#", "E", -1)
    with pytest.raises(FindChordError):
        find_note_positions_on_string("E", "E#", 12)
