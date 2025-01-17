"""

@Author: Philip Yawen Guo

@ This repository is to automatic sitiching rota images

"""



import os
import glob

import numpy as np
import cv2
from numpy import float32
import matplotlib.pyplot as plt
from scipy.signal import correlate
from Rota_stitching.box_pairing import box_pairing

def skimage2opencv(src):
    src *= 255
    src.astype(int)
    cv2.cvtColor(src,cv2.COLOR_RGB2BGR)
    return src

def opencv2skimage(src):
    cv2.cvtColor(src,cv2.COLOR_BGR2RGB)
    src.astype(float32)
    src = src/255
    return src

def read_img(path):

    """
    extract the corresponding images for each patients from folders
    :param path: path of the folder which contains all images
    :return: paths after filtering and sorting
    """

    subjects_path = os.listdir(path)
    IDs = []
    for subject_path in subjects_path:
        name = subject_path[:subject_path.index("_")+8]
        if name not in IDs:
            IDs.append(name)

    image_paths = []
    for i in range(len(IDs)):
        each_pairs = [0,0,0,0,0]
        # L:mac;opt  R: opt; mac
        for subject in subjects_path:
            # image seq: rota_opt; raw_opt; rota_mac; raw_mac; name
            if "_L_" in subject:
                if IDs[i] in subject and "_L_Opt" in subject:
                    each_pairs[0] = subject + "/" + subject[:-3] + "RMapEnSumRNFL_3Resized.png"
                    each_pairs[1] = subject + "/" + "EnfaceAdjusted.png"
                if IDs[i] in subject and "_L_Mac" in subject:
                    each_pairs[2] = subject + "/" + subject[:-3] + "RMapEnSumRNFL_3Resized.png"
                    each_pairs[3] = subject + "/" + "EnfaceAdjusted.png"
                if IDs[i] in subject:
                    each_pairs[4] = IDs[i]+"_L_"
        image_paths.append(each_pairs)

        each_pairs = [0,0,0,0,0]
        for subject in subjects_path:
            # image seq: rota_mac; raw_mac; rota_opt; raw_opt; name
            if "_R_" in subject:
                if IDs[i] in subject and "_R_Mac" in subject:
                    each_pairs[0] = subject + "/" + subject[:-3] + "RMapEnSumRNFL_3Resized.png"
                    each_pairs[1] = subject + "/" + "EnfaceAdjusted.png"
                if IDs[i] in subject and "_R_Opt" in subject:
                    each_pairs[2] = subject + "/" + subject[:-3] + "RMapEnSumRNFL_3Resized.png"
                    each_pairs[3] = subject + "/" + "EnfaceAdjusted.png"
                if IDs[i] in subject:
                    each_pairs[4] = IDs[i]+"_R_"
        image_paths.append(each_pairs)
    return image_paths

path = "./Export GEN Extracted 20200513/"
image_paths = read_img(path)
if __name__ == '__main__':



    """
    Step 2:
    Features searching
    """

    ks = 50
    moving_coors=box_pairing(mac_opt_vessel_imgs[0],mac_opt_vessel_imgs[1],ks,10,3)

    for i in range(len(moving_coors)):
        moving_coors[i] = int(moving_coors[i])
    print(moving_coors)

    """
    Step 3:
    Calcuating the transforming vector and Moving images
    """

    imgs = []
    img1 = cv2.imread(path + each_image_paths[0])
    img2 = cv2.imread(path + each_image_paths[2])
    imgs = [img1,img2]
    x1 = 100
    y1 = 100
    x2 = 100 + len(imgs[0])
    y2 = 100

    x_movestep = moving_coors[3] + (len(imgs[0][0])-moving_coors[1])
    y_movestep = moving_coors[0] - moving_coors[2]
    canvas = np.ones((800,600,3),dtype=np.uint8)*255
    if "_L_" in each_image_paths[4]:
        canvas[y1:y1+len(imgs[0]),x1:x1+len(imgs[0][0]),:] = imgs[0]
        canvas[y2+y_movestep:y2+len(imgs[1])+y_movestep,x2-x_movestep:x2-x_movestep+len(imgs[1][0]),:] = imgs[1]
    else:
        canvas[y2+y_movestep:y2+len(imgs[1])+y_movestep,x2-x_movestep:x2-x_movestep+len(imgs[1][0]),:] = imgs[1]
        canvas[y1:y1+len(imgs[0]),x1:x1+len(imgs[0][0]),:] = imgs[0]


np.save("error_result.npy",error_list)