# coding:utf-8
# from db.redis_db import Proxys
# from db.basic_db import proxy_db_session
# from db.models import Proxys
# from db.redis_db import Proxys_Redis
# from page_parse.proxy import get_proxy_to_db
# from page_get.basic import get_page
# from utils.random_gen import random_event_occur
from page_parse.taobaomm import get_image_by_uid
from db.models import MMPic
from db.mm_info import insert_mm_pic, check_hash_exist

# test code
if __name__ == '__main__':
	test_list = []
	# print(get_image_by_uid('390324964'))
	mmpic = MMPic()
	mmpic.uid = 1
	test_list.append(mmpic)
	mmpic = MMPic()
	mmpic.uid = 2
	test_list.append(mmpic)
	insert_mm_pic(test_list)
	print(check_hash_exist(1, 1, 1, 1))
# end