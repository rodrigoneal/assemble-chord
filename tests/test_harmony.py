import pytest

from src.assemble_chord.app.core.harmony.enums import HarmonicTypes
from src.assemble_chord.app.core.harmony.music import (
    detect_music_keys,
    dominant_secondary,
    harmonic_field_with_function,
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


@pytest.mark.parametrize(
    "tonica,tipo,esperado",
    [
        (
            "C",
            "maior",
            {
                "I": ("C7M", "Tonica"),
                "ii": ("Dm7", "Subdominante"),
                "iii": ("Em7", "Tonica"),
                "IV": ("F7M", "Subdominante"),
                "V": ("G7", "Dominante"),
                "vi": ("Am7", "Tonica"),
                "viiø": ("Bm7(b5)", "Dominante"),
            },
        ),
        (
            "D",
            "maior",
            {
                "I": ("D7M", "Tonica"),
                "ii": ("Em7", "Subdominante"),
                "iii": ("F#m7", "Tonica"),
                "IV": ("G7M", "Subdominante"),
                "V": ("A7", "Dominante"),
                "vi": ("Bm7", "Tonica"),
                "viiø": ("C#m7(b5)", "Dominante"),
            },
        ),
        (
            "E",
            "maior",
            {
                "I": ("E7M", "Tonica"),
                "ii": ("F#m7", "Subdominante"),
                "iii": ("G#m7", "Tonica"),
                "IV": ("A7M", "Subdominante"),
                "V": ("B7", "Dominante"),
                "vi": ("C#m7", "Tonica"),
                "viiø": ("D#m7(b5)", "Dominante"),
            },
        ),
    ],
)
def test_campo_maior(tonica, tipo, esperado):
    resultado = harmonic_field_with_function(tonica, tipo)
    assert resultado == esperado


@pytest.mark.parametrize(
    "tonica,tipo,esperado",
    [
        (
            "C",
            "menor_natural",
            {
                "i": ("Cm7", "Tonica"),
                "iiø": ("Dm7(b5)", "Subdominante"),
                "III": ("Eb7M", "Tonica"),
                "iv": ("Fm7", "Subdominante"),
                "v": ("Gm7", "Dominante"),
                "VI": ("Ab7M", "Tonica"),
                "VII": ("Bb7", "Dominante"),
            },
        ),
        (
            "A",
            "menor_natural",
            {
                "i": ("Am7", "Tonica"),
                "iiø": ("Bm7(b5)", "Subdominante"),
                "III": ("C7M", "Tonica"),
                "iv": ("Dm7", "Subdominante"),
                "v": ("Em7", "Dominante"),
                "VI": ("F7M", "Tonica"),
                "VII": ("G7", "Dominante"),
            },
        ),
    ],
)
def test_campo_menor_natural(tonica, tipo, esperado):
    resultado = harmonic_field_with_function(tonica, tipo)
    assert resultado == esperado


@pytest.mark.parametrize(
    "tonica,tipo,esperado",
    [
        (
            "C",
            "menor_harmonico",
            {
                "i": ("Cm7", "Tonica"),
                "iiø": ("Dm7(b5)", "Subdominante"),
                "III+": ("Eb7M(#5)", "Tonica"),
                "iv": ("Fm7", "Subdominante"),
                "V": ("G7", "Dominante"),
                "VI": ("Ab7M", "Tonica"),
                "vii°": ("Bm7(b5)", "Dominante"),
            },
        ),
        (
            "G",
            "menor_harmonico",
            {
                "i": ("Gm7", "Tonica"),
                "iiø": ("Am7(b5)", "Subdominante"),
                "III+": ("Bb7M(#5)", "Tonica"),
                "iv": ("Cm7", "Subdominante"),
                "V": ("D7", "Dominante"),
                "VI": ("Eb7M", "Tonica"),
                "vii°": ("F#m7(b5)", "Dominante"),
            },
        ),
    ],
)
def test_campo_menor_harmonico(tonica, tipo, esperado):
    resultado = harmonic_field_with_function(tonica, tipo)
    assert resultado == esperado


@pytest.mark.parametrize(
    "tonica,tipo,esperado",
    [
        (
            "C",
            "menor_melodico",
            {
                "i": ("Cm7", "Tonica"),
                "ii": ("Dm7", "Subdominante"),
                "III+": ("Eb7M(#5)", "Tonica"),
                "IV": ("F7", "Subdominante"),
                "V": ("G7", "Dominante"),
                "viø": ("Am7(b5)", "Tonica"),
                "viiø": ("Bm7(b5)", "Dominante"),
            },
        ),
        (
            "B",
            "menor_melodico",
            {
                "i": ("Bm7", "Tonica"),
                "ii": ("C#m7", "Subdominante"),
                "III+": ("D7M(#5)", "Tonica"),
                "IV": ("E7", "Subdominante"),
                "V": ("F#7", "Dominante"),
                "viø": ("G#m7(b5)", "Tonica"),
                "viiø": ("A#m7(b5)", "Dominante"),
            },
        ),
    ],
)
def test_campo_menor_melodico(tonica, tipo, esperado):
    resultado = harmonic_field_with_function(tonica, tipo)
    assert resultado == esperado


@pytest.mark.parametrize("tonica", ["C", "D", "F#", "Bb"])
def test_campo_maior_varias_tonicas(tonica):
    # Apenas garante que todos os graus retornam algo válido
    resultado = harmonic_field_with_function(tonica, "maior")
    assert set(resultado.keys()) == {"I", "ii", "iii", "IV", "V", "vi", "viiø"}
    # Verifica que cada valor é uma tupla (acorde, função) válida
    assert all(
        isinstance(v, tuple)
        and len(v) == 2
        and all(isinstance(x, str) and x for x in v)
        for v in resultado.values()
    )
