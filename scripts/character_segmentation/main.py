import os
import sys
import cv2
import filters
import utilities
from tqdm import tqdm


def process_images(license_plates, show_index=-1):
    license_plate_annotations = []

    for index, (image, plate_number) in tqdm(enumerate(license_plates)):
        show = True if index == show_index else False

        original = utilities.resize(image, dims=(800, 200), show=show, title="original")
        image = original.copy()

        image = filters.denoise(image, blur_method="bilateral", kernel=15, sigma=20, show=show, title="bilateral-blur")
        image = filters.binarize(image, inverted=True, adaptive=False, show=show)
        image = filters.denoise(image, blur_method="median", kernel=3, show=show, title="median-blur")
        image = filters.get_canny_edges(image, show=show)

        image_title = "img_" + str(index) + ".jpg"
        bboxes = utilities.get_bboxes(image, original.copy(), threshold_w=2.5, threshold_h=0.25, show=show, save=False, title=image_title)

        license_plate_annotations.append((original.copy(), plate_number, bboxes))
        if show:
            if cv2.waitKey(0) & 0xFF == 27:
                cv2.destroyAllWindows()

    return license_plate_annotations


def find_accuracy(license_plate_annotations, show=False, save=False):
    correct = 0
    partial = 0

    for (image, plate_number, bboxes) in license_plate_annotations:
        if len(plate_number) == len(bboxes):
            image_filepath = os.path.join(".", "datasets", "correct_images", str(plate_number) + ".jpg")
            if save:
                utilities.save_image(image, image_filepath)
            correct += 1
        else:
            image_filepath = os.path.join(".", "datasets", "wrong_images", str(plate_number) + ".jpg")
            if save:
                utilities.save_image(image, image_filepath)
        partial += 1 - abs(len(plate_number) - len(bboxes)) / len(plate_number)

    accuracy_license_plate = (correct / len(license_plate_annotations)) * 100
    accuracy_characters = (partial / len(license_plate_annotations)) * 100

    if show:
        print("total accuracy = {:.2f}%".format(accuracy_license_plate))
        print("accuracy per plate = {:.2f}%".format(accuracy_characters))

    return accuracy_license_plate, accuracy_characters


def main(image_folder_path):
    license_plates = []
    for filename in os.listdir(image_folder_path):
        image_path = os.path.join(image_folder_path, filename)
        image = utilities.get_image(image_path)
        plate_number = filename.split(".")[0]
        license_plates.append((image, plate_number))

    license_plate_annotations = process_images(license_plates, show_index=1)
    accuracy_license_plate, accuracy_characters = find_accuracy(license_plate_annotations, show=True, save=True)


if __name__ == "__main__":
    image_folder_path = sys.argv[1]
    main(image_folder_path)