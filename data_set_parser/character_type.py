import os
from enum import Enum


class CharacterType(Enum):
    LOWER_CASE = 0
    UPPER_CASE = 1
    LOWER_CASE_CURSIVE = 2
    UPPER_CASE_CURSIVE = 3

    @staticmethod
    def from_folder_name(parent_folder: str, folder_name: str) -> "CharacterType":
        parent = os.path.basename(parent_folder).lower()
        child = folder_name.lower()

        if parent == "pisane" and child == "male":
            return CharacterType.LOWER_CASE_CURSIVE
        elif parent == "pisane" and child == "velike":
            return CharacterType.UPPER_CASE_CURSIVE
        elif parent == "tiskane" and child == "male":
            return CharacterType.LOWER_CASE
        elif parent == "tiskane" and child == "velike":
            return CharacterType.UPPER_CASE
        else:
            raise ValueError(f"Unknown folder combination: {parent}/{child}")