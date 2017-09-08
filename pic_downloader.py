# coding:utf-8
from db.mm_info import fetch_pic_info_from_given_id, update_pic_dl_status, get_max_id_in_mmpic, get_min_id_in_mmpic
import os
from urllib.request import urlretrieve
from urllib.error import HTTPError

from multiprocessing import Pool

from random import randint

output_path = 'D:\\Project\\TaommPic\\0906_001\\raw'   # 保存路径
num = 5000                                             # 目标下载量
new_dl_flag = 1                         
old_dl_flag = 0

core_num = 4

def download_and_save_pic(path, num, new_dl_flag=1, old_dl_flag=0):
    min_id = get_min_id_in_mmpic()
    max_id = get_max_id_in_mmpic()
    random_id = randint(min_id, max_id)
    pic_list = fetch_pic_info_from_given_id(random_id, num, old_dl_flag)
    for pic in pic_list:
        output_user_path = os.path.join(output_path, str(pic.uid))
        if not os.path.exists(output_user_path):
            os.makedirs(output_user_path)
        local_path = os.path.join(output_user_path, pic.hash + '.jpg')
        dl_url = 'http:' + pic.pic_url
        try:
            urlretrieve(dl_url, local_path)
            print('Download ' + local_path + ' Success' + ' in ' + str(os.getpid()))
            update_pic_dl_status(pic.id, new_dl_flag)
        except HTTPError as err:  
            print(err)

if __name__ == "__main__":
    p = Pool(core_num)
    for i in range(4):
        p.apply_async(download_and_save_pic, args=(output_path, num, new_dl_flag, old_dl_flag,))
    p.close()
    p.join()
    # download_and_save_pic(output_path, num, new_dl_flag, old_dl_flag)
    