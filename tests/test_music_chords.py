import pytest

from src.assemble_chord.app.core.music_chords.decode import decode_chords
from src.assemble_chord.app.core.music_chords.get_chord import get_chord_in_banana


@pytest.mark.asyncio
async def test_se_busca_acorde_no_site_banana():
    resultado = await get_chord_in_banana("C")

    assert "@" in resultado.text


@pytest.mark.parametrize(
    "input_string, expected_output",
    [
        ("C", [2, 0, 1, 2]),
        ("D", [4, 2, 3, 4]),
        ("E", [2, 1, 0, 2]),
        ("F#m7(b5)", [2, 2, 1, 2]),
    ],
)
@pytest.mark.asyncio
async def test_se_decodifica_o_acorde(input_string, expected_output):
    response = await get_chord_in_banana(input_string)
    resultado = decode_chords(response.text)
    assert expected_output in resultado
