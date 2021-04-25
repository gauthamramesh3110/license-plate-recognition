"""
SCRIPT SYNTAX:
> python get_frames.py <path_to_video_folder> <path_to_save_frames>
"""


import sys
import cv2
import os
from tqdm import tqdm

def get_frames(open_path, save_path):
    
    for filename in tqdm(os.listdir(open_path)):
        frameCount = 0
        os.mkdir(os.path.join(save_path + filename.split('.')[0]))

        if filename.split('.')[1].lower() in ['mp4', 'mov']:

            video_path = os.path.join(open_path, filename)
            videoObj = cv2.VideoCapture(video_path)

            while videoObj.isOpened():
                
                success, image = videoObj.read()

                if success:
                    saved_name = "frame_" + str(frameCount) + ".jpg"
                    cv2.imwrite(os.path.join(save_path, filename.split('.')[0], saved_name), image)
                    frameCount += 1
                else:
                    break
            
            videoObj.release()
            cv2.destroyAllWindows()
    

if __name__ == '__main__':

    if(len(sys.argv) < 3):
        print('ERROR: NOT ENOUGH ARGUMENTS')
        print('getframes <video-path> <save-path>')

    open_path = sys.argv[1]
    save_path = sys.argv[2]

    get_frames(open_path, save_path)

