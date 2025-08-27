import pytest

from src.assemble_chord.app.core.chordfy.chord_utils.intervals import Intervalos


@pytest.mark.parametrize(
    "valor, descricao_esperada",
    [
        (0, (1, None)),
        (1, (2, "b")),
        (4, (3, None)),
        (7, (5, None)),
        (11, (7, None)),
    ],
)
def test_descricao_valores_validos(valor, descricao_esperada):
    assert Intervalos.descricao(valor).nome == descricao_esperada


@pytest.mark.parametrize("valor", [12, -1])
def test_descricao_valores_invalidos(valor):
    assert Intervalos.descricao(valor) is None


@pytest.mark.parametrize("valor", range(12))
def test_descricao_todos_intervalos(valor):
    desc = Intervalos.descricao(valor)
    assert desc is not None, f"Intervalo {valor} não tem descrição"
