import os
import sys
import glob
import pandas as pd
import xml.etree.ElementTree as ET


def xml_to_csv(path):
    xml_list = []
    for xml_file in glob.glob(path + "/*.xml"):
        tree = ET.parse(xml_file)
        root = tree.getroot()
        for member in root.findall("object"):
            value = (
                root.find("filename").text,
                int(root.find("size")[0].text),
                int(root.find("size")[1].text),
                member[0].text,
                int(member[4][0].text),
                int(member[4][1].text),
                int(member[4][2].text),
                int(member[4][3].text),
            )
            xml_list.append(value)
    column_name = ["filename", "width", "height", "class", "xmin", "ymin", "xmax", "ymax"]
    xml_df = pd.DataFrame(xml_list, columns=column_name)
    return xml_df


def main(data_dirpath):
    for directory in ["train", "test"]:
        image_path = os.path.join(data_dirpath, directory, "annotations-xml")
        xml_df = xml_to_csv(image_path)
        csv_savepath = os.path.join(data_dirpath, directory, "annotations-csv")
        if not os.path.isdir(csv_savepath):
            os.mkdir(csv_savepath)
        xml_df.to_csv(os.path.join(csv_savepath, '{}.csv'.format(directory)), index=None)
        print("Successfully converted xml to csv.")


if __name__ == "__main__":
    main(sys.argv[1])