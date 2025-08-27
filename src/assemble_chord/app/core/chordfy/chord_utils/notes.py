class Notas:
    CHROMATIC_SHARP = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
    CHROMATIC_FLAT = ["C", "Db", "D", "Eb", "E", "F", "Gb", "G", "Ab", "A", "Bb", "B"]

    NOTE_TO_SEMITONE = {
        "C": 0,
        "C#": 1,
        "Db": 1,
        "D": 2,
        "D#": 3,
        "Eb": 3,
        "E": 4,
        "F": 5,
        "F#": 6,
        "Gb": 6,
        "G": 7,
        "G#": 8,
        "Ab": 8,
        "A": 9,
        "A#": 10,
        "Bb": 10,
        "B": 11,
    }

    @classmethod
    def para_semitom(cls, nota: str) -> int:
        """Converte nota em semitom"""
        if nota not in cls.NOTE_TO_SEMITONE:
            raise ValueError(f"Nota inválida: {nota}")
        return cls.NOTE_TO_SEMITONE[nota]

    @classmethod
    def para_nota(
        cls, semitom: int, prefer_sharp: bool = True, old_chord: str | None = None
    ) -> str:
        """
        Converte semitom em nota, respeitando preferencia por # ou b.
        Usa CHROMATIC_SHARP ou CHROMATIC_FLAT de acordo com prefer_sharp.
        """
        semitom = semitom % 12
        if prefer_sharp:
            chord = cls.CHROMATIC_SHARP[semitom]
            if old_chord and old_chord not in chord:
                return cls.CHROMATIC_FLAT[semitom]
            return chord
        else:
            return cls.CHROMATIC_FLAT[semitom]
