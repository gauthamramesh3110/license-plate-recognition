from sys import argv
import cv2
import pytesseract
import sys
import numpy as np
from scipy.ndimage import interpolation as inter
import os
from tqdm import tqdm


def correct_skew(image, delta=1, limit=5):
    def determine_score(arr, angle):
        data = inter.rotate(arr, angle, reshape=False, order=0)
        histogram = np.sum(data, axis=1)
        score = np.sum((histogram[1:] - histogram[:-1])**2)
        return histogram, score

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    thresh = cv2.threshold(gray, 0, 255,
                           cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

    scores = []
    angles = np.arange(-limit, limit + delta, delta)
    for angle in angles:
        histogram, score = determine_score(thresh, angle)
        scores.append(score)

    best_angle = angles[scores.index(max(scores))]

    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, best_angle, 1.0)
    rotated = cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_CUBIC, \
              borderMode=cv2.BORDER_REPLICATE)

    # cv2.imshow('skew corrected', rotated)
    return best_angle, rotated


def get_image(image_path):
    image = cv2.imread(image_path)
    # cv2.imshow('original', image)
    return image


def get_grayscale(image):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # cv2.imshow('grayscale', image)
    return image


def resize(image, scale_hor, scale_ver):
    image = cv2.resize(image, (0, 0),
                       fx=scale_hor,
                       fy=scale_ver,
                       interpolation=cv2.INTER_CUBIC)
    # cv2.imshow('resized', image)
    return image


def denoise(image):
    # image = cv2.GaussianBlur(image, (3, 3), 0)
    # image = cv2.medianBlur(image, 3)
    image = cv2.bilateralFilter(image, 15, 75, 75)
    # cv2.imshow('denoise', image)
    return image


def binarize(image):
    image = cv2.threshold(image, 0, 255,
                          cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
    # cv2.imshow('binary', image)
    return image


def dilate(image, kernel_size):
    kernel = np.ones(kernel_size, np.uint8)
    image = cv2.dilate(image, kernel, iterations=1)
    # cv2.imshow('dilate', image)
    return image


def erode(image, kernel_size):
    kernel = np.ones(kernel_size, np.uint8)
    image = cv2.erode(image, kernel, iterations=1)
    # cv2.imshow('erode', image)
    return image


def opening(image):
    kernel = np.ones((9, 9), np.uint8)
    image = cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)
    # cv2.imshow('opening', image)
    return image


def invert(image):
    image = cv2.bitwise_not(image)
    # cv2.imshow('inverted', image)
    return image


def canny(image):
    image = cv2.Canny(image, 30, 200)
    # cv2.imshow('canny', image)
    return image


def contours(image):
    cnt, _ = cv2.findContours(image, cv2.RETR_EXTERNAL,
                              cv2.CHAIN_APPROX_SIMPLE)
    cnt = sorted(cnt, key=cv2.contourArea)
    return cnt


def sort_by_area(bbox):
    (x, y, w, h) = bbox
    return w * h


def draw_bounding_boxes(image, cnt):
    image_height, image_width = image.shape
    max_area = 0
    max_height = 0
    bounding_boxes = []
    for c in cnt:
        x, y, w, h = cv2.boundingRect(c)
        if w / h > 1.2:
            continue
        if w / h < 0.2:
            continue

        area = w * h
        max_area = max(max_area, area)
        max_height = max(max_height, h)
        bounding_boxes.append((x, y, w, h, area))

    bounding_boxes = list(
        filter(lambda x: x[4] > 0.4 * max_area, bounding_boxes))

    for (x, y, w, h, area) in bounding_boxes:
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 0))

    # cv2.imshow('bbox', image)
    return image, bounding_boxes, max_height


def ocr(image):
    custom_config = r'-c tessedit_char_whitelist=0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ --oem 3 --psm 7'
    output = pytesseract.image_to_string(image,
                                         lang='eng',
                                         config=custom_config)
    return output


def get_boxes(image):
    custom_config = r'-c tessedit_char_whitelist=0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ --oem 3 --psm 7'
    boxes = pytesseract.image_to_boxes(image, lang='eng', config=custom_config)
    return boxes


def draw_new_image(image, bounding_boxes, max_height, count):
    sub_count = 0
    char_basename = 'IMG_' + str(count)

    bounding_boxes = sorted(bounding_boxes, key=lambda x: x[0])
    spacer = np.ones((max_height, 40), np.uint8) * 255
    new_image = spacer.copy()
    for (x, y, w, h, area) in bounding_boxes:
        char_filename = char_basename + '_' + str(sub_count) + '.jpg'
        sub_count += 1

        char = image[y:y + h, x:x + w]
        cv2.imwrite(os.path.join('characters', char_filename), char)
        new_w = int((w / h) * max_height)
        char = cv2.resize(char, (new_w, max_height))

        # new_image = np.concatenate((new_image, char), axis=1)
        # new_image = np.concatenate((new_image, spacer), axis=1)

        new_image = cv2.hconcat([new_image, char])
        new_image = cv2.hconcat([new_image, spacer])

    # cv2.imshow('new', new_image)
    # new_image  = Image.fromarray(new_image)
    return new_image


def main(image_path, count, filename):

    image = get_image(image_path)
    _, image = correct_skew(image)
    image = get_grayscale(image)
    image = resize(image, 4, 3)
    image = binarize(image)
    image = denoise(image)

    image = erode(image, (3, 3))
    image = dilate(image, (3, 3))

    cny = canny(image)
    cnt = contours(cny)
    image = invert(image)

    bnd_image, bounding_boxes, max_height = draw_bounding_boxes(
        image.copy(), cnt)

    new_image = None

    if len(bounding_boxes) >= 8 and len(bounding_boxes) <= 10:
        new_image = draw_new_image(image, bounding_boxes, max_height, count)
        cv2.imwrite(os.path.join('processed_plates', filename), new_image)
        # image = resize(image, 1.5, 1.5)
        count += 1
        # cv2.imshow('final', image)

    # output = ocr(new_image)
    # print(output)
    # boxes = get_boxes(image)
    # print(len(output))
    # print(boxes)

    if cv2.waitKey(0) & 0xff == 27:
        cv2.destroyAllWindows()

    return count


if __name__ == '__main__':
    dir = sys.argv[1]
    count = 0
    for filename in tqdm(os.listdir(dir)):
        filepath = os.path.join(dir, filename)
        count = main(filepath, count, filename)

    print(count)