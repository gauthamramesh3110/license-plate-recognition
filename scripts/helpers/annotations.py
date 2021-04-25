import xml.etree.ElementTree as et

def __get_voc(annotation:dict) -> et.ElementTree:
    annotation_root = et.Element('annotation')

    # FILENAME
    filename = et.Element('filename')
    filename.text = annotation['filename']
    annotation_root.append(filename)
    # END OF FILENAME

    # SIZE
    size = et.Element('size')

    width = et.Element('width')
    width.text = annotation['width']
    size.append(width)

    height = et.Element('height')
    height.text = annotation['height']
    size.append(height)

    depth = et.Element('depth')
    depth.text = annotation['depth']
    size.append(depth)

    annotation_root.append(size)
    # END OF SIZE

    # OBJECT
    for object in annotation['objects']:
        object_root = et.Element('object')

        name = et.Element('name')
        name.text = object['name']
        object_root.append(name)

        pose = et.Element('pose')
        pose.text = 'Unspecified'
        object_root.append(pose)

        truncated = et.Element('truncated')
        truncated.text = '0'
        object_root.append(truncated)

        difficult = et.Element('difficult')
        difficult.text = '0'
        object_root.append(difficult)

        bndbox = et.Element('bndbox')

        xmin = et.Element('xmin')
        xmin.text = object['xmin']
        bndbox.append(xmin)

        xmax = et.Element('xmax')
        xmax.text = object['xmax']
        bndbox.append(xmax)

        ymin = et.Element('ymin')
        ymin.text = object['ymin']
        bndbox.append(ymin)

        ymax = et.Element('ymax')
        ymax.text = object['ymax']
        bndbox.append(ymax)

        object_root.append(bndbox)
        annotation_root.append(object_root)
    # END OF OBJECT

    xml_tree = et.ElementTree(annotation_root)
    return xml_tree

# TODO: Add functions for TXT and CSV formats

def save_annotation(annotation:dict, savepath:str, type:str):
    if type == 'voc':
        xml_tree = __get_voc(annotation)
        
        with open(savepath, 'wb') as file:
            xml_tree.write(file)
        