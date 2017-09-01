# -*-coding:utf-8 -*-
from page_get.basic import get_page
from db.models import MMInfo, MMPic
from utils.hash_gen import md5_gen
import re
import json
from db.mm_info import get_ids_by_home_flag_random, insert_mm_pic

def get_mm_info(url):
	html = get_page(url, user_verify=False, need_login=False)
	model_pattern = re.compile('''<a class="lady-name" href="(.*?)".*>(.*?)</a>''', re.U)
	items = re.findall(model_pattern, html)
	db_info_items = []
	for item in items:
		mminfo = MMInfo()
		mminfo.uid = item[0].split('=')[1]
		mminfo.name = item[1]
		db_info_items.append(mminfo)
	return db_info_items

def get_album_lsit_by_uid(uid, page=1):
	album_url_tpl = 'https://mm.taobao.com/self/album/open_album_list.htm?_charset=utf-8&user_id%20={0}&page={1}'
	album_url = album_url_tpl.format(uid, page)
	html = get_page(album_url, user_verify=False, need_login=False)
	if '没有照片' in html:
		return []
	album_pattern = re.compile('''.*album_id=(.*?)&.*''', re.U)
	items = re.findall(album_pattern, html)
	return list(set(items))

def get_image_by_uid(uid):
	cur_album_page = 1
	cur_photo_page = 1
	photo_num = 0

	max_user_photo = 150

	image_url_tpl = 'https://mm.taobao.com/album/json/get_album_photo_list.htm?user_id={0}&album_id={1}&page={2}'
	while photo_num <= max_user_photo:
		album_list = get_album_lsit_by_uid(uid, cur_album_page)
		if album_list != []:
			for album in album_list:
				cur_photo_page = 1
				while True:
					if photo_num >= max_user_photo:
						return True
					image_url = image_url_tpl.format(uid, album, cur_photo_page)
					html = get_page(image_url, user_verify=False, need_login=False)
					cont = json.loads(html, encoding='utf-8')
					pic_class_list = []
					if cont['isError'] == '0':
						pic_list = cont['picList']
						if pic_list:
							pic_list_len = len(pic_list)
							photo_num = photo_num + pic_list_len
							for pic in pic_list:
								mmpic = MMPic()
								mmpic.uid = uid
								mmpic.album_id = album
								mmpic.pic_id = pic['picId']
								mmpic.pic_url = pic['picUrl']
								mmpic.pic_url = mmpic.pic_url.replace('jpg_290x10000.jpg', 'jpg_620x10000.jpg')
								mmpic.hash = md5_gen(str(uid) + str(album) + str(mmpic.pic_id))
								mmpic.dl_flag = 0
								mmpic.judge_flag = 0
								pic_class_list.append(mmpic)
							insert_mm_pic(pic_class_list)
						cur_photo_page = cur_photo_page + 1
					else:
						break
		else:
			return True
		cur_album_page = cur_album_page + 1
