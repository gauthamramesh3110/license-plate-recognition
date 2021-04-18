import sys
import pandas as pd
import os

def txt_to_df(annotation_path) -> pd.DataFrame:

    txt_list = []
    column_headers = ['filename', 'width', 'height', 'class', 'xmin', 'ymin', 'xmax', 'ymax']

    for filename in os.listdir(annotation_path):
        # print(filename.split('.')[-1])
        if filename.split('.')[-1] != 'txt':
            continue
 
        filepath = os.path.join(annotation_path, filename)

        # print(filepath)
        with open(filepath, 'r') as f:
            value = f.readline().split()
            value.insert(3, 'license_plate')
            # print(value)
            txt_list.append(value)
        
    txt_df = pd.DataFrame(txt_list, columns=column_headers)
    return txt_df

def main(dataset_path, save_path):
    for dir in ['test', 'train']:
        annotation_path = os.path.join(dataset_path, dir)
        csv_path = os.path.join(save_path, dir + '.csv')
        txt_df = txt_to_df(annotation_path)
        txt_df.to_csv(csv_path, index=None)

    print('Successfully converted xml to csv.')

if __name__ == '__main__':
    dataset_path = sys.argv[1]
    save_path = sys.argv[2]
    main(dataset_path, save_path)