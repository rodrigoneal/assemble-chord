from music21 import pitch


def samba_progression(root_note: str, mode="major"):
    """
    Retorna a progressão típica de samba I–VI–II–V para maior,
    ou i–V7–iv–V7 para menor.
    """
    root = pitch.Pitch(root_note)

    if mode == "major":
        I = root.name  # noqa: E741
        VI = root.transpose(9).name + "7"  # 6ª grau dominante
        II = root.transpose(2).name + "m"  # 2ª grau menor
        V = root.transpose(7).name + "7"  # 5ª grau dominante
        return [I, VI, II, V]

    elif mode == "minor":
        i = root.name + "m"
        V7 = root.transpose(0).name + "7"  # dominante do menor
        iv = root.transpose(5).name + "m"  # 4ª grau menor
        V7_final = root.transpose(7).name + "7"  # dominante principal
        return [i, V7, iv, V7_final]

    else:
        raise ValueError("Mode deve ser 'major' ou 'minor'")
