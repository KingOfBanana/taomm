# coding:utf-8
import hashlib

def md5_gen(str, encode='utf-8'):
	md5 = hashlib.md5()
	md5.update(str.encode(encode))
	return md5.hexdigest()