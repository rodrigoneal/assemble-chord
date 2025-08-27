import pytest

from src.assemble_chord.app.core.chordfy.find import find_note_positions_on_string


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
