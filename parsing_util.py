import cv2

import imutils
import numpy as np

from character_type import CharacterType
from constants import *

DEBUG = False


def parse_image(file_path, character_type, debug=False):
    global DEBUG
    DEBUG = debug

    file_name = os.path.basename(file_path)
    image = cv2.imread(file_path, cv2.IMREAD_COLOR)

    if image is None:
        print(f"Failed to read image: {file_name}")
        return

    # Grid roi max and min size.
    max_area_size = int(GRID_H * GRID_W * 1.3)
    min_area_size = int(GRID_H * GRID_W * 0.7)

    ROI = get_ROI(image, min_area_size, max_area_size, GRID_W, GRID_H)
    w, h, c = ROI.shape
    print(f"Page {file_name} ROI size: ({w}, {h}, {c})  (original: {image.shape})")

    if DEBUG:
        resized_ROI = cv2.resize(ROI, (int(h * 0.4), int(w * 0.4)))
        cv2.imshow("grid_roi", resized_ROI)
        cv2.waitKey()
        cv2.destroyAllWindows()

    parse_characters_from_grid(file_name, ROI, character_type)

    # parsing validation.
    verify_output(file_name, character_type)
    cv2.destroyAllWindows()


def parse_characters_from_grid(file_name, grid, char_type: CharacterType):
    global DEBUG
    grid_h, grid_w, c = grid.shape

    # Grid dimensions.
    CELL_W = grid_w // GRID_COLUMNS
    CELL_H = grid_h // GRID_ROWS

    CHAR_ROI_W_BUFFER = int(CELL_W * 0.5)
    CHAR_ROI_H_BUFFER = int(CELL_H * 0.5)

    # Iterate through grid.
    row_count = 1
    for y in range(0, grid_h, CELL_H):
        if row_count > GRID_ROWS:
            break

        column_number = 1
        for x in range(0, grid_w, CELL_W):
            if column_number > GRID_COLUMNS:
                break

            # Crop char ROI with buffer.
            y_start = max(0, int(y - CHAR_ROI_H_BUFFER))
            y_end = y_start + CELL_H + 2 * CHAR_ROI_H_BUFFER

            x_start = max(0, int(x - CHAR_ROI_W_BUFFER))
            x_end = x_start + CELL_W + 2 * CHAR_ROI_W_BUFFER

            cropped_char = grid[y_start: y_end, x_start: x_end]

            # Crop square roi from straight lines.
            roi = square_roi(cropped_char, CELL_W, CELL_H, CHAR_ROI_W_BUFFER)

            if DEBUG:
                cv2.imshow("roi", roi)
                cv2.imshow("c_char", cropped_char)
                cv2.waitKey()
                cv2.destroyAllWindows()

            output_path = get_output_path(char_type, file_name, column_number, row_count)
            cv2.imwrite(output_path, roi)
            column_number += 1

        row_count += 1


def get_ROI(image, area_min_size, area_max_size, cell_w, cell_h):
    rotated_image = rotate_image_based_on_area(image, area_min_size, area_max_size)
    contour = find_ROI_contour(rotated_image, area_min_size, area_max_size)

    if contour is None:
        if area_min_size > cell_w * cell_h * 0.7:
            return get_ROI(image, area_min_size - 1, area_max_size, cell_w, cell_h)

        return rotated_image[0:cell_h, 0:cell_w]
        pass

    x, y, w, h = cv2.boundingRect(contour)
    ROI = rotated_image[y:y + h, x:x + w]
    return ROI


def square_roi(image, roi_w, roi_h, roi_buffer):
    global DEBUG

    # Detect vertical and horizontal lines in roi.
    edges = cv2.Canny(image, 50, 150)
    lines = cv2.HoughLinesP(edges, 1, np.pi / 180, threshold=30, minLineLength=roi_h - roi_buffer,
                            maxLineGap=roi_h)
    vertical = []
    horizontal = []

    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]

            if abs(x1 - x2) < 10:
                vertical.append((x1, y1, x2, y2))
            elif abs(y1 - y2) < 10:
                horizontal.append((x1, y1, x2, y2))

        if DEBUG:
            cropped_char_cp = image.copy()
            for line in lines:
                x1, y1, x2, y2 = line[0]  # unpack

                cv2.line(cropped_char_cp, (x1, y1), (x2, y2), (0, 255, 0), 2)

            cv2.imshow("Detected Lines", cropped_char_cp)

    TOLERANCE = 15

    # Starting values.
    x_left, x_right = 0, roi_w
    y_top, y_bottom = 0, roi_h

    # Find vertical edge pair (distance should be around height width).
    found_v = False
    for i in range(len(vertical)):
        for j in range(i + 1, len(vertical)):
            # Get x-coordinates (averaging start/end to be safe)
            x_i = (vertical[i][0] + vertical[i][2]) / 2
            x_j = (vertical[j][0] + vertical[j][2]) / 2

            dist = abs(x_i - x_j)
            if abs(dist - roi_w) <= TOLERANCE:
                x_left = int(min(x_i, x_j))
                x_right = int(max(x_i, x_j))
                found_v = True
                break
        if found_v: break

    # Find horizontal edge pair (distance should be around width width).
    found_h = False
    for i in range(len(horizontal)):
        for j in range(i + 1, len(horizontal)):
            # Get y-coordinates (averaging start/end to be safe)
            y_i = (horizontal[i][1] + horizontal[i][3]) / 2
            y_j = (horizontal[j][1] + horizontal[j][3]) / 2

            dist = abs(y_i - y_j)
            if abs(dist - roi_h) <= TOLERANCE:
                y_top = int(min(y_i, y_j))
                y_bottom = int(max(y_i, y_j))
                found_h = True
                break
        if found_h: break

    # Crop the ROI
    if y_bottom > y_top and x_right > x_left:
        return image[y_top + GRID_EDGE_WIDTH:y_bottom - GRID_EDGE_WIDTH,
               x_left + GRID_EDGE_WIDTH:x_right - GRID_EDGE_WIDTH]


def rotate_image_based_on_area(image, area_min_size, area_max_size):
    contour = find_ROI_contour(image, area_min_size, area_max_size)

    if contour is None:
        return image

    # Find bounding box and extract ROI
    rect = cv2.minAreaRect(contour)
    (center, size, angle) = rect

    if angle < -45:
        angle += 90

    return imutils.rotate(image, angle)


def find_ROI_contour(image, area_min_size, area_max_size):
    global DEBUG
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)

    _, thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (15, 15))
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    max_area = -1
    best_cnt = None
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        area = w * h
        if area_min_size < area < area_max_size and area > max_area:
            max_area = area
            best_cnt = cnt

    if DEBUG:
        debug_contours(gray, contours, area_min_size, area_max_size)

    if best_cnt is None:
        return None

    # Get mask
    x, y, w, h = cv2.boundingRect(best_cnt)
    mask = np.zeros(gray.shape, np.uint8)
    cv2.rectangle(mask, (x + GRID_EDGE_WIDTH, y + GRID_EDGE_WIDTH),
                  (x + w - GRID_EDGE_WIDTH, y + h - GRID_EDGE_WIDTH),
                  255, -1)

    out = np.zeros_like(gray)
    out[mask == 255] = gray[mask == 255]
    blur = cv2.GaussianBlur(out, (5, 5), 0)
    thresh = cv2.adaptiveThreshold(blur, 255, 1, 1, 11, 2)

    if DEBUG:
        cv2.imshow("thresh", thresh)
        cv2.imshow("mask", mask)
        cv2.waitKey()

    # Find contour and sort by contour area
    cnts = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]

    if len(cnts) > 0:
        return max(cnts, key=cv2.contourArea)

    return None


def verify_output(file_name, character_type: CharacterType):
    missing = []

    for column_number in CHARACTER_FILE_NAMES:
        path = get_output_path(character_type, file_name, column_number, 50)
        if not os.path.exists(path):
            missing.append(path)

    if missing:
        print(f"\nMissing {len(missing)} file(s) for {file_name} ({character_type.name}):")
        for p in missing:
            print(f"  MISSING: {p}")
    else:
        print(f"\nAll char crops present for {file_name} ({character_type.name})")


def get_output_path(char_type: CharacterType, file_name, column_number, row_count):
    return os.path.join(OUTPUT_DIR, CHARACTER_SUBFOLDERS[char_type.value],
                        f"{file_name}_{CHARACTER_FILE_NAMES[column_number][char_type.value]}_{row_count}.png")


def debug_contours(gray, contours, area_min_size, area_max_size):
    all_areas = sorted([w * h for cnt in contours for x, y, w, h in [cv2.boundingRect(cnt)]], reverse=True)
    print(f"Area not found. min={area_min_size} max={area_max_size} | top bounding rect areas: {all_areas[:5]}")

    # Draw top 10 contours
    contours_with_area = sorted(
        [(w * h, cnt) for cnt in contours for x, y, w, h in [cv2.boundingRect(cnt)]],
        key=lambda x: x[0], reverse=True
    )
    colors = [
        (255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (0, 255, 255),
        (255, 0, 255), (128, 0, 0), (0, 128, 0), (0, 0, 128), (128, 128, 0)
    ]
    debug_image = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
    for i, (area, cnt) in enumerate(contours_with_area[:10]):
        x, y, w, h = cv2.boundingRect(cnt)
        color = colors[i]
        cv2.drawContours(debug_image, [cnt], -1, color, 3)
        cv2.rectangle(debug_image, (x, y), (x + w, y + h), color, 2)
        cv2.putText(debug_image, f"#{i + 1} {area}", (x, y - 5),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

    scale = 0.3
    resized = cv2.resize(debug_image, (int(debug_image.shape[1] * scale), int(debug_image.shape[0] * scale)))
    cv2.imshow("Top 10 Contours (no match found)", resized)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
