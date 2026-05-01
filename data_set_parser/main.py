import csv
import sys
import time

from characteristics import parse_characteristics, get_characteristics_file_name
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

        file_name = get_characteristics_file_name(N, M)

        if os.path.exists(file_name):
            os.remove(file_name)

        path = os.path.join(os.path.join(os.path.abspath(os.path.dirname(__file__)), DATA_SET_FOLDER))
        os.makedirs(path, exist_ok=True)

        now = time.time()
        with open(DATA_SET_FOLDER + file_name, mode='a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            parse_folder(folder_path, lambda path, char_type: parse_characteristics(path, writer, N, M))
        print(f"{time.time() - now} seconds")
    elif mode == '-ci':
        N = int(sys.argv[2])
        M = int(sys.argv[3])
        image_path = sys.argv[4]

        file_name = get_characteristics_file_name(N, M)
        os.makedirs(DATA_SET_FOLDER, exist_ok=True)

        with open(DATA_SET_FOLDER + file_name, mode='a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            parse_characteristics(image_path, writer, N, M)
