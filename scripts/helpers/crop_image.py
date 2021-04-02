"""
This script takes annotation data from space separated values and crops to that bounding box.
The annotations are in the following format: 
    <image_name> <width> <height> <xmin> <ymin> <xmax> <ymax>
The script takes the following parameters: 
    <annotation_path> <image_path> <save_path>

    python crop_image.py ..\datasets\extracted\license-plate-car-cropped\annotations\ ..\datasets\extracted\license-plate-car-cropped\images\ ..\datasets\extracted\license-plate-cropped
"""
import sys
import os
from PIL import Image
from tqdm import tqdm


def crop_and_save(image_filepath, bbox_cood, save_filepath):
    [xmin, ymin, xmax, ymax] = bbox_cood

    image = Image.open(image_filepath)
    cropped_image = image.crop((xmin, ymin, xmax, ymax))
    cropped_image.save(save_filepath)


def get_bbox_cood(annotation_filepath):

    with open(annotation_filepath) as file:
        attributes = file.read().split(' ')

        filename = attributes[0]
        bbox_cood = list(map(int, attributes[3:]))

        if len(bbox_cood) != 4:
            raise AssertionError

        return filename, bbox_cood


def main(annotation_path, image_path, save_path):

    for annotation_filename in tqdm(os.listdir(annotation_path)):
        annotation_filepath = os.path.join(annotation_path,
                                           annotation_filename)
        image_filename, bbox_cood = get_bbox_cood(annotation_filepath)
        image_filepath = os.path.join(image_path, image_filename)
        save_filepath = os.path.join(save_path, image_filename)
        crop_and_save(image_filepath, bbox_cood, save_filepath)


if __name__ == '__main__':

    if len(sys.argv) < 4:
        print('Insufficent arguments. See below for argument format:')
        print(
            'python crop_image.py <annotation_path> <image_path> <save_path>')
        exit()

    # GET ALL ARGUMENT VALUES
    annotation_path = sys.argv[1]
    image_path = sys.argv[2]
    save_path = sys.argv[3]

    # CHECK IF ANNOTATION AND IMAGE PATHS EXIST
    path_error = False

    if not os.path.exists(annotation_path):
        print('Annotation path doesn\'t exist. Please check.')

    if not os.path.exists(image_path):
        print('Image path doesn\'t exist. Please check.')

    if path_error:
        exit()

    # CREATE SAVE FOLDER IF IT DOESN'T EXIST
    if not os.path.exists(save_path):
        os.mkdir(save_path)

    main(annotation_path, image_path, save_path)