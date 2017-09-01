# coding:utf-8
from db.mm_info import fetch_pic_info, update_pic_dl_status
import os
from urllib.request import urlretrieve

output_path = 'D:\\Project\\TaommPic'
num = 1000
new_dl_flag = 1
old_dl_flag = 0

pic_list = fetch_pic_info(num, old_dl_flag)
for pic in pic_list:
    output_user_path = os.path.join(output_path, str(pic.uid))
    if not os.path.exists(output_user_path):
        os.makedirs(output_user_path)
    local_path = os.path.join(output_user_path, pic.hash + '.jpg')
    dl_url = 'http:' + pic.pic_url
    try:
        urlretrieve(dl_url, local_path)
        print('Download ' + local_path + ' Success!')
        update_pic_dl_status(pic.id, new_dl_flag)
    except urllib.error.HTTPError as err:  
        print(err)
    