import pytest

from src.assemble_chord.app.core.harmony.music import (
    detect_music_keys,
    dominant_secondary,
)
from src.assemble_chord.app.core.harmony.samba import samba_progression
from src.assemble_chord.app.exceptions.harmony import SambaProgressionError


@pytest.mark.parametrize(
    "nota,tom,esperado",
    [("C", "major", ["C", "A7", "Dm", "G7"]), ("A", "minor", ["Am", "A7", "Dm", "E7"])],
)
def test_se_cria_quadradinho_samba(nota, tom, esperado):
    resultado = samba_progression(nota, tom)
    assert resultado == esperado


def test_se_gera_erro_quando_modo_invalido():
    with pytest.raises(SambaProgressionError) as excinfo:
        samba_progression("C", "dorian")
    assert "Mode deve ser 'major' ou 'minor'" in str(excinfo.value)


@pytest.mark.parametrize(
    "seq, esperado",
    [
        (
            ["Gm", "G7", "Cm", "F7", "Bb", "Eb", "Am7b5", "D7"],
            "Gm",
        ),
        (
            ["G", "G7M", "Bm7", "Em7", "C", "Am7", "D7", "G", "G7M"],
            "G",
        ),
        (["A", "E/G#", "A", "B7"], "A"),
        (["F#m7", "G#m7", "A7M", "B7(4)", "C#7(4)"], "E"),
    ],
)
def test_se_pega_o_tom_da_musica(seq, esperado):
    resultado = detect_music_keys(seq)  # só passa a sequência como entrada
    assert any(esperado in tom for tom in resultado)


@pytest.mark.parametrize(
    "acorde,proximo,tonalidade,esperado",
    [
        # Dominantes secundários (acorde fora da escala, maior com 7)
        ("D7", "Gm", "Bb", "V7/vi"),
        ("E7", "Am", "C", "V7/vi"),
        ("A7", "Dm", "C", "V7/ii"),
        ("F#7", "Bm", "E", "V7/v"),
        # Acordes diatônicos (dentro da escala)
        ("Bb", "Eb", "Bb", "I"),
        ("F7", "Bb", "Bb", "V7/i"),
        ("Gm", "Cm", "Bb", "vi"),
        ("Cm", "F7", "Bb", "ii"),
        # Acordes menores com sétima não são tratados como dominantes secundários
        ("Am7", "Dm7", "C", "vi7"),
        ("Dm7", "G7", "C", "ii7"),
        # Maior simples dentro da tonalidade
        ("C", "F", "C", "I"),
        ("G", "C", "C", "V"),
        # Teste com acorde diminuto (diatônico)
        ("Bdim", "C", "C", "viio"),
    ],
)
def test_dominant_secondary(acorde, proximo, tonalidade, esperado):
    resultado = dominant_secondary(acorde, proximo, tonalidade)
    assert resultado == esperado
