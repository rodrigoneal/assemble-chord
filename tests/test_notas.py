# import pytest
# from src.assemble_chord.app.core.chordfy.chord_utils.notes import Notas


# @pytest.mark.parametrize(
#     "nota, esperado",
#     [
#         ("C", 0),
#         ("C#", 1),
#         ("Db", 1),
#         ("D", 2),
#         ("D#", 3),
#         ("Eb", 3),
#         ("E", 4),
#         ("F", 5),
#         ("F#", 6),
#         ("Gb", 6),
#         ("G", 7),
#         ("G#", 8),
#         ("Ab", 8),
#         ("A", 9),
#         ("A#", 10),
#         ("Bb", 10),
#         ("B", 11),
#     ],
# )
# def test_para_semitom_valido(nota, esperado):
#     assert Notas.para_semitom(nota) == esperado

# @pytest.mark.parametrize("nota", ["H", "", "Do"])
# def test_para_semitom_invalido(nota):
#     assert Notas.para_semitom(nota) is None


# def test_para_nota_valido():
#     # 0 a 11 devem retornar notas válidas
#     assert Notas.para_nota(0) in ["C", "C#", "Db"]  # dependendo do mapeamento
#     assert Notas.para_nota(1) in ["C#", "Db"]
#     assert Notas.para_nota(11) == "B"


# def test_para_nota_com_valores_maiores_que_11():
#     # Deve fazer módulo 12
#     assert Notas.para_nota(12) == Notas.para_nota(0)
#     assert Notas.para_nota(13) == Notas.para_nota(1)
#     assert Notas.para_nota(-1) == Notas.para_nota(11)


# @pytest.mark.parametrize(
#     "nota",
#     [
#         "C",
#         "C#",
#         "Db",
#         "D",
#         "D#",
#         "Eb",
#         "E",
#         "F",
#         "F#",
#         "Gb",
#         "G",
#         "G#",
#         "Ab",
#         "A",
#         "A#",
#         "Bb",
#         "B",
#     ],
# )
# def test_bidirecionalidade(nota):
#     # Garantir que uma nota convertida para semitom e de volta retorna a nota original (ou equivalente enharmônica)
#     semitom = Notas.para_semitom(nota)
#     assert 0 <= semitom <= 11
#     back = Notas.para_nota(semitom)
#     assert isinstance(back, str)
