import pytest

from src.assemble_chord.app.core.harmony.samba import samba_progression


@pytest.mark.parametrize(
    "nota,tom,esperado",
    [("C", "major", ["C", "A7", "Dm", "G7"]), ("A", "minor", ["Am", "A7", "Dm", "E7"])],
)
def test_se_cria_quadradinho_samba(nota, tom, esperado):
    resultado = samba_progression(nota, tom)
    assert resultado == esperado
