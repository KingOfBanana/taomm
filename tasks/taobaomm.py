# -*-coding:utf-8 -*-
from page_parse.taobaomm import get_image_by_uid
from db.mm_info import get_ids_by_home_flag_random, insert_mm_pic, update_seed_crawled_status

def excute_crawl_mm_info():
	seed_ids = get_ids_by_home_flag_random(0, 2000)
	for seed_id in seed_ids:
		get_image_by_uid(seed_id.uid)
		# insert_mm_pic(mm_info_pics)
		update_seed_crawled_status(seed_id.uid, 1)