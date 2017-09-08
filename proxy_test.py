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
from db.mm_info import fetch_pic_info_from_given_id

# test code
if __name__ == '__main__':
	print(fetch_pic_info_from_given_id(110000, 10, 0))
# end