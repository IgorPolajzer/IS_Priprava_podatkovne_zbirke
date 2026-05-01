from character_type import CharacterType
from constants import *


def ensure_output_dirs():
    for sub_folder in CHARACTER_SUBFOLDERS:
        path = os.path.join(OUTPUT_DIR, sub_folder)
        os.makedirs(path, exist_ok=True)


def parse_folder(folder_path, function):
    ensure_output_dirs()
    sub_folders = os.listdir(folder_path)

    for folder in sub_folders:
        sub_folder_path = os.path.join(folder_path, folder)
        if not os.path.isdir(sub_folder_path):
            continue

        # Iterate over male/velike inside pisane/tiskane
        for child_folder in os.listdir(sub_folder_path):
            child_folder_path = os.path.join(sub_folder_path, child_folder)

            # Skip the izjeme folder.
            if child_folder.lower() == "izjeme":
                continue

            if not os.path.isdir(child_folder_path):
                continue

            character_type = CharacterType.from_folder_name(sub_folder_path, child_folder)

            image_files = [
                os.path.join(child_folder_path, f)
                for f in os.listdir(child_folder_path)
                if f.endswith(".png")
            ]

            for file_path in image_files:
                function(file_path, character_type)
