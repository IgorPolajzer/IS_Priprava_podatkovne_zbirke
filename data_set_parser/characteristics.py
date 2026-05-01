import cv2
import os
from constants import CHAR_MAP


def parse_characteristics(image_path, csv_writer, columns, rows):
    # Load image.
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if image is None:
        print(f"Failed to read image: {image_path}")
        return

    # Threshold so counting char pixels is counting nonzero values.
    _, thresh = cv2.threshold(image, 127, 255, cv2.THRESH_BINARY_INV)

    h, w = thresh.shape

    # Ensure columns and rows are integers
    columns = int(columns)
    rows = int(rows)

    cell_h = h // rows
    cell_w = w // columns

    features = []
    for r in range(rows):
        for c in range(columns):
            y1 = r * cell_h
            y2 = (r + 1) * cell_h if r < rows - 1 else h

            x1 = c * cell_w
            x2 = (c + 1) * cell_w if c < columns - 1 else w

            quadrant = thresh[y1:y2, x1:x2]
            dark_pixels = cv2.countNonZero(quadrant)
            total_pixels = quadrant.size

            # Ratio of char pixels to total pixels in quadrant
            ratio = dark_pixels / total_pixels if total_pixels > 0 else 0
            features.append(round(ratio, 4))

    # Extract label from filename
    # Format: {file_name}_{char_internal_name}_{row_count}.png
    basename = os.path.basename(image_path)
    char_label = "Unknown"

    for char in CHAR_MAP:
        if f"_{char}_tiskane_" in basename:
            char_label = CHAR_MAP[char] + "_t"
            break
        elif f"_{char}_pisane_" in basename:
            char_label = CHAR_MAP[char] + "_p"
            break

    # Save to CSV
    csv_writer.writerow(features + [char_label])

def get_characteristics_file_name(n, m):
    return f"characteristics_{n}_{m}.csv"