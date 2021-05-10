import os

import cv2

from BoundingRectangle import BoundingRectangle

INPUT_FILENAME = "./pics/test.jpg"
OUTPUT_FILENAME = "./output.jpg"


def crop(image_path, output_path):
    img = cv2.imread(image_path)
    saturation_plane = img[:, :, 1]  # Extract just the saturation plane from image.
    _, thresh = cv2.threshold(saturation_plane, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)  # Apply threshold to image

    # Remove noise
    dilate = cv2.dilate(thresh, None)
    erode = cv2.erode(dilate, None)

    # Find contours in the threshold image.
    contours, hierarchy = cv2.findContours(erode, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)

    biggest_contour = BoundingRectangle(0, 0, 0, 0)
    for index, contour in enumerate(contours):
        if is_highest_hierarchy(index, hierarchy):
            x, y, w, h = cv2.boundingRect(contour)
            current = BoundingRectangle(x, y, w, h)
            biggest_contour = biggest_contour if biggest_contour.area() >= current.area() else current

    cropped_image = img[biggest_contour.top:biggest_contour.bottom, biggest_contour.left:biggest_contour.right]
    cv2.imwrite(output_path, cropped_image)


def is_highest_hierarchy(index, hierarchy_list):
    return hierarchy_list[0, index, 3] != -1

ORIGINAL_DIR = "./original"
OUTPUT_DIR = "./output"

if __name__ == "__main__":
    for root, dirs, names in os.walk(ORIGINAL_DIR):
        for name in names:
            crop(os.path.join(root, name), os.path.join(OUTPUT_DIR, name))
