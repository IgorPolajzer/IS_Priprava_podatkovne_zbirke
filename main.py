import sys

from characteristics import parse_characteristics
from file_util import *
from parsing_util import parse_image

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: python main.py -pi <image_path> OR python main.py -pf <folder_path>")
        sys.exit(1)

    mode = sys.argv[1]

    if mode == '-pi':
        image_path = sys.argv[2]
        parse_image(image_path, CharacterType.LOWER_CASE_CURSIVE, debug=True)
    elif mode == '-pf':
        folder_path = sys.argv[2]
        parse_folder(folder_path, parse_image)
    elif mode == '-cf':
        N = int(sys.argv[2])
        M = int(sys.argv[3])
        folder_path = sys.argv[4]

        if os.path.exists(FEATURES_CSV):
            os.remove(FEATURES_CSV)

        parse_folder(folder_path, lambda path, char_type: parse_characteristics(path, N, M))
    elif mode == '-ci':
        N = int(sys.argv[2])
        M = int(sys.argv[3])
        image_path = sys.argv[4]

        if os.path.exists(FEATURES_CSV):
            os.remove(FEATURES_CSV)

        parse_characteristics(image_path, N, M)
