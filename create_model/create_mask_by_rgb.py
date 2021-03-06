import os

import numpy as np
import pandas as pd
import tifffile as tiff
from skimage import morphology

# water 0,108,255
# tree 0,168,62
# playground 102,34,153
# road 112,112,112
# building_yard 255, 255, 255
# bare_land 242, 155, 118
# general_building 249,255,25
# countryside 227,22,33
# factory 48,254,254
# shadow 255,0,255

dic_class = dict()
dic_class['water'] = [48, 93, 254]
dic_class['tree'] = [12, 169, 64]
dic_class['playground'] = [102, 17, 151]
dic_class['road'] = [111, 111, 111]
dic_class['building_yard'] = [255, 255, 255]
dic_class['bare_land'] = [239, 156, 119]
dic_class['general_building'] = [249, 255, 25]
dic_class['countryside'] = [227, 22, 33]
dic_class['factory'] = [48, 254, 254]
dic_class['shadow'] = [255, 1, 255]

# 一般建筑&农村&工厂&阴影
# 运动场&道路
# 水体&植被
# 运动场&道路
# 建筑场地&裸地
tag_name = 'split-mask-data'
class_name = 'general_building'


def get_mask(img, img_class):
    width, height = img.shape[:2]
    channel = 3
    msk = np.zeros((width, height, channel))

    for w in range(width):
        for h in range(height):
            if np.array_equal(dic_class[img_class], img[w][h]):
                msk[w][h] = [255, 255, 255]
    return msk


# Dir = "/home/yokoyang/PycharmProjects/untitled/896_biaozhu"
Dir = "/home/yokoyang/PycharmProjects/untitled/896_val"


def get_files_name(file_dir):
    L = []
    for root, dirs, files in os.walk(file_dir):
        for file in files:
            if os.path.splitext(file)[1] == '.tif':
                L.append(os.path.splitext(file)[0])
    return L


def image2csv(img_folder_name, dir_name, csv_name):
    L = get_files_name(img_folder_name)
    df = pd.DataFrame()
    df['ImageId'] = L
    df.to_csv(dir_name + "/" + csv_name, index=False, header=True)


img_folder_name = Dir + '/' + tag_name
image2csv(img_folder_name, Dir, "2.csv")
train_img = pd.read_csv(Dir + '/2.csv')

Image_ID = sorted(train_img.ImageId.unique())

for i, img_id in enumerate(Image_ID):
    print(i)
    filename = os.path.join(Dir, tag_name, '{}.tif'.format(img_id))
    # img = cv2.imread(filename)
    # img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = tiff.imread(filename)
    msk_file_name = os.path.join(Dir, class_name, '{}.tif'.format(img_id))
    msk_img = get_mask(img, class_name)
    # cv2.imwrite(msk_file_name, msk_img)
    msk_img = msk_img > 1
    ms = msk_img[:, :, 1]
    dst = morphology.remove_small_objects(ms, min_size=10, connectivity=1)
    dst = dst.astype(np.uint8)
    msk_img = msk_img.astype(np.float32)
    dst ^= 1
    msk_img = msk_img.astype(np.uint8)
    msk_img[:, :, 0] = dst[:, :] * 255
    msk_img[:, :, 1] = dst[:, :] * 255
    msk_img[:, :, 2] = dst[:, :] * 255
    tiff.imsave(msk_file_name, msk_img)
    # fig, (ax1, ax2) = plt.subplots(1, split-mask-data, figsize=(8, 4))
    # ax1.imshow(ms, plt.cm.gray, interpolation='nearest')
    # ax2.imshow(dst, plt.cm.gray, interpolation='nearest')
    # fig.tight_layout()
    # plt.show()
