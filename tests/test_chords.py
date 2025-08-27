import pytest

from src.assemble_chord.app.core.chordfy.chord_utils.chords import Acordes


@pytest.mark.parametrize(
    "entrada, esperado",
    [
        ("7M", "maj7"),  # deve traduzir para alias
        ("M7", "maj7"),  # alias alternativo
        ("m7b5", "m7(5-)"),  # alias alternativo
        ("ø", "m7(5-)"),  # alias alternativo
        ("maj7", "maj7"),  # já está na forma final
        ("m7", "m7"),  # sem alias, retorna igual
        ("", ""),  # string vazia
    ],
)
def test_traduz_qualidade(entrada, esperado):
    assert Acordes.traduz_qualidade(entrada) == esperado
