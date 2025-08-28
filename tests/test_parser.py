import pytest

from src.assemble_chord.app.core.chordfy.parser import parser_bemol, simplify_chord


@pytest.mark.parametrize(
    "input,expected",
    [
        ("G#m7(5-)", "G#m"),
        ("F#m7M", "F#m"),
        ("C°", "Cdim"),
        ("E4", "E"),
        ("E7(9)", "E"),
        ("Eb4(7/9)", "Eb"),
    ],
)
def test_se_simplifica_acorde(input, expected):
    assert simplify_chord(input) == expected


@pytest.mark.parametrize(
    "input,expected",
    [("Ab", "A-"), ("Db", "D-"), ("Gb", "G-"), ("Cb", "C-"), ("Fm7b9", "Fm7b9")],
)
def test_se_muda_b_para_menos(input, expected):
    assert parser_bemol(input) == expected
