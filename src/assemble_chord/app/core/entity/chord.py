from typing import Annotated

from pydantic import BaseModel, BeforeValidator


def just_letter(name: str) -> str:
    return "".join(filter(str.isalpha, name))


class Note(BaseModel):
    name: Annotated[str, BeforeValidator(just_letter)]
    note_accidental: str | None = None
    degree: int
    degree_accidental: str | None = None

    @property
    def is_root(self):
        return self.degree == 1


class ChordEntity(BaseModel):
    root: str
    chord: str
    notes: list[Note]
    quality: str | None = None
    bass: str | None = None

    @property
    def all_notes(self):
        return [f"{note.name}{note.note_accidental or ''}" for note in self.notes]
