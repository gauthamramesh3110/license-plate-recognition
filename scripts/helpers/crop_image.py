import sys
import os
import annotations
from PIL import Image
from tqdm import tqdm
import xml.etree.ElementTree as et

def get_from_voc(filepath) -> dict:

    annotation = dict()

    tree = et.parse(filepath)
    root = tree.getroot()

    annotation['filename'] = root.find('./filename').text
    annotation['width'] = root.find('./size/width').text
    annotation['height'] = root.find('./size/height').text
    annotation['depth'] = root.find('./size/depth').text
    annotation['objects'] = []

    for object in root.findall('./object'):
        annotation['objects'].append({
            'name': object.find('./name').text,
            'xmin': object.find('./bndbox/xmin').text,
            'xmax': object.find('./bndbox/xmax').text,
            'ymin': object.find('./bndbox/ymin').text,
            'ymax': object.find('./bndbox/ymax').text,
        })
    
    return annotation

def find_object_index(objects, object_name:str) -> int:

    for index, object in enumerate(objects):
        if object['name'] == object_name:
            return index
    
    return -1


def main(image_folderpath, annotation_folderpath, save_folderpath):
    image_save_folderpath = os.path.join(save_folderpath, 'images')
    annotation_save_folderpath = os.path.join(save_folderpath, 'annotations')

    if not os.path.isdir(image_save_folderpath):
        os.mkdir(image_save_folderpath)
    if not os.path.isdir(annotation_save_folderpath):
        os.mkdir(annotation_save_folderpath)

    for annotation_filename in tqdm(os.listdir(annotation_folderpath)):
        annotation_filepath = os.path.join(annotation_folderpath, annotation_filename)
        annotation = get_from_voc(annotation_filepath)

        image_filename = annotation['filename']
        image_filepath = os.path.join(image_folderpath, image_filename)

        car_object_index = find_object_index(annotation['objects'], 'car')
        licenseplate_object_index = find_object_index(annotation['objects'], 'license_plate')

        xmin = int(annotation['objects'][car_object_index]['xmin'])
        xmax = int(annotation['objects'][car_object_index]['xmax'])
        ymin = int(annotation['objects'][car_object_index]['ymin'])
        ymax = int(annotation['objects'][car_object_index]['ymax'])
        
        xmin_lp = int(annotation['objects'][licenseplate_object_index]['xmin'])
        xmax_lp = int(annotation['objects'][licenseplate_object_index]['xmax'])
        ymin_lp = int(annotation['objects'][licenseplate_object_index]['ymin'])
        ymax_lp = int(annotation['objects'][licenseplate_object_index]['ymax'])

        annotation['objects'][licenseplate_object_index]['xmin'] = str(xmin_lp - xmin)
        annotation['objects'][licenseplate_object_index]['xmax'] = str(xmax_lp - xmin)
        annotation['objects'][licenseplate_object_index]['ymin'] = str(ymin_lp - ymin)
        annotation['objects'][licenseplate_object_index]['ymax'] = str(ymax_lp - ymin)

        annotation['objects'].pop(car_object_index)

        annotation['width'] = str(xmax-xmin)
        annotation['height'] = str(ymax-ymin)

        image = Image.open(image_filepath)
        image = image.crop((xmin, ymin, xmax, ymax))
        
        annotation_save_filename = image_filename.split('.')[0] + '.xml'
        annotation_save_filepath = os.path.join(annotation_save_folderpath, annotation_save_filename)
        annotations.save_annotation(annotation, annotation_save_filepath, 'voc')

        image_save_filepath = os.path.join(image_save_folderpath, image_filename)
        image.save(image_save_filepath)

if __name__ == '__main__':
    image_folderpath = sys.argv[1]
    annotation_folderpath = sys.argv[2]
    save_folderpath = sys.argv[3]

    main(image_folderpath, annotation_folderpath, save_folderpath)