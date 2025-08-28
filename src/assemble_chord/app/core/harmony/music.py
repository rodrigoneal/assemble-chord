from collections import defaultdict

from music21 import harmony, key, roman, stream

from src.assemble_chord.app.core.chordfy.parser import (
    CAMPOS,
    PESOS,
    RELATIVOS,
    parser_standard_chord_name,
    simplify_chord,
)
from src.assemble_chord.app.core.chordfy.util import get_bass
from src.assemble_chord.app.exceptions.harmony import NotaInvalidaError


def detect_music_keys(acordes, margem=1.0):
    """
    Detecta os tons mais prováveis combinando music21 + pesos.
    Retorna lista de (tom, modo, pontuação).
    """
    # Normaliza acordes para music21
    acordes_norm = []
    acordes_simplificados = []
    for c in acordes:
        acordes_simplificados.append(simplify_chord(c))
        try:
            bass = get_bass(c)
            acordes_norm.append(
                harmony.ChordSymbol(parser_standard_chord_name(c, bass))
            )
        except Exception:
            raise NotaInvalidaError(f"Acorde inválido: {c}")

    # Análise pelo music21
    s = stream.Stream(acordes_norm)
    k = s.analyze("key")
    tonic_base = k.tonic.name
    mode_base = k.mode

    # Calcula scores usando PESOS
    scores = defaultdict(float)
    for tom, campo in CAMPOS.items():
        # Tom maior
        for idx, acorde in enumerate(campo):
            for a in acordes_simplificados:
                if a == acorde.replace("dim", "") or a == acorde:
                    scores[(tom, "maior")] += PESOS[idx]

        # Tom menor relativo
        relativo = RELATIVOS[tom]
        for idx, acorde in enumerate(campo):
            for a in acordes_simplificados:
                if a == acorde.replace("dim", "") or a == acorde:
                    scores[(relativo, "menor")] += PESOS[idx]

    # Adiciona o tom sugerido pelo music21 com leve bônus
    scores[(tonic_base, mode_base)] += 0.5

    if not scores:
        return []

    # Máxima pontuação
    max_score = max(scores.values())

    # Retorna candidatos próximos da máxima
    candidatos = [
        (tom, modo, score)
        for (tom, modo), score in scores.items()
        if max_score - score <= margem
    ]

    return sorted(candidatos, key=lambda x: -x[2])


def dominant_secondary(acorde: str, proximo_acorde: str, tonalidade: str) -> str:
    """
    Transforma acorde dominante fora da escala em função musical (V7/X)
    """
    acorde = parser_standard_chord_name(acorde)
    proximo_acorde = parser_standard_chord_name(proximo_acorde)
    tonalidade = parser_standard_chord_name(tonalidade)

    t = key.Key(tonalidade)
    c = harmony.ChordSymbol(acorde)

    # Se o acorde é maior com sétima e fora da escala → possível dominante secundária
    if c.quality in ["dominant", "major"] and c.seventh:
        alvo = harmony.ChordSymbol(proximo_acorde)
        # Determina o grau relativo do acorde seguinte na tonalidade
        rn_alvo = roman.romanNumeralFromChord(alvo, t)
        return f"V7/{rn_alvo.figure.lower()}"
    else:
        # Caso diatônico, retorna numeral normal
        rn = roman.romanNumeralFromChord(c, t)
        return rn.figure
