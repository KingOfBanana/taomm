# coding:utf-8
from db.basic_db import mm_db_session
from db.models import MMInfo, MMPic
from decorators.decorator import mm_db_commit_decorator
from sqlalchemy import func

def check_uid_exist(uid):
	r = mm_db_session.query(MMInfo).filter(MMInfo.uid == uid).first()
	if r:
		return True
	return False

def check_hash_exist(uid, album_id, pic_id, hash):
	r = mm_db_session.query(MMPic).filter(MMPic.hash == hash).first()
	if r:
		check_r = mm_db_session.query(MMPic).filter(MMPic.uid == uid).filter(MMPic.album_id == album_id).filter(MMPic.pic_id == pic_id).first()
		if check_r:
			return True
	return False

@mm_db_commit_decorator
def insert_mm_info(mm_items):
	if mm_items:
	    for item in mm_items:
	    	if item:
	    		if check_uid_exist(item.uid) == False:
	        		mm_db_session.add(item)
	    mm_db_session.commit()

@mm_db_commit_decorator
def insert_mm_pic(mm_items):
	if mm_items:
	    for item in mm_items:
	    	if item:
	    		if check_hash_exist(item.uid, item.album_id, item.pic_id, item.hash) == False:
	        		mm_db_session.add(item)
	    mm_db_session.commit()

@mm_db_commit_decorator
def update_seed_crawled_status(uid, new_status):
	r = mm_db_session.query(MMInfo).filter(MMInfo.uid == uid).first()
	if r:
		r.home_crawled = new_status
	mm_db_session.commit()

def get_ids_by_home_flag_random(status = 0, num = 100):
    return mm_db_session.query(MMInfo).filter(MMInfo.home_crawled == status).order_by(func.random()).limit(num).all()

def fetch_pic_info(num, status=0):
	r = mm_db_session.query(MMPic).filter(MMPic.dl_flag == status).limit(num).all()
	if r:
		return r
	else:
		return []

@mm_db_commit_decorator
def update_pic_dl_status(id, new_status=1):
	r = mm_db_session.query(MMPic).filter(MMPic.id == id).first()
	if r:
		r.dl_flag = new_status
	mm_db_session.commit()

def get_max_id_in_mmpic():
	r = mm_db_session.query(func.max(MMPic.id)).all();
	if r:
		return r[0][0]

def get_min_id_in_mmpic():
	r = mm_db_session.query(func.min(MMPic.id)).all();
	if r:
		return r[0][0]

# select * where id >= input limit num
def fetch_pic_info_from_given_id(given_id, num, status=0):
	r = mm_db_session.query(MMPic).filter(MMPic.id >= given_id).filter(MMPic.dl_flag == status).limit(num).all()
	if r:
		return r
	else:
		return []
