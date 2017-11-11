#!/usr/bin/python  
# -*- coding: utf-8 -*-
import requests,json,socket
from bs4 import BeautifulSoup
import random,os  
import sys
import re
import argparse
import time

workingDir = os.path.dirname(os.path.abspath('.'))
# Mkdir for picture
picDir = workingDir + '\\picture'
if not os.path.exists(picDir):
	os.mkdir(picDir)
valid_type = ['.png', '.jpg', '.PNG', '.JPG', '.gif', '.GIF', '.jpeg', '.JPEG']

def retriveUrl(keyWord='test',amount=20):
	"""
	利用关键字从百度图片下载对应图片链接
	:param keyWord: 搜索关键字
	:param amount: 搜索数量
	:return:
	"""
	url_list = list()
	NumPic = 60
	baseUrl = 'http://image.baidu.com/search/flip?tn=baiduimage&ie=utf-8&word=' + keyWord + '&pn='
	pattern = re.compile(r'\"objURL\":\"(.*?)\"')
	for page in range(int(amount/NumPic)+1):
		Url = baseUrl + str(page)
		print('Fetching Url form Baidu pic')
		try:
			req = requests.get(Url).text
		except:
			print('This Baidu Pic Page cannot reach')
			continue
		url_list += pattern.findall(req)
		time.sleep(0.5)
	return url_list

def retrivePic(raw_data,dir='temp',amount=20 , abs_dir = ''):
	"""
	从指定链接获取图片，并保持在指定位置,按照数字命名排序
	:param raw_data: 图片链接或是图片链接的list，链接为str格式
	:param dir: 文件保存相对路径，不填写放在temp中
	:param amount: 指定最大的下载数量
	:param abs_dir: 文件保存绝对路径，填写取消dir
	:return:
	"""
	# Check the input
	assert (type(dir) == str) and (type(amount) == int) and (type(raw_data) in (str, list))
	if type(raw_data) == str:
		data = list()
		data.append(raw_data)
	else:
		data = raw_data
	counter = 1
	# Mkdir and change working dir
	patternFileFormat = re.compile(r'.*(\..*?)$')

	if not abs_dir == '':
		FilePath = abs_dir
	else:
		if not dir.startswith('\\'):
			dir = '\\' + dir + '\\'
		FilePath = picDir + dir
	if not os.path.exists(FilePath):
		try:
			os.mkdir(FilePath)
		except:
			print('Cannot Create Dir!')
			return
	os.chdir((FilePath))
	# Main loop for retriving pic
	for url in data:
		# Check the file format from url
		# And Check if the format is valid
		try:
			fileFormat = patternFileFormat.findall(url.split('/')[-1])[0]
			print(fileFormat)
			if fileFormat not in valid_type:
				raise Exception
		except:
			print('Not a valid format. Fetch Next')
			continue
		# Fetch pictures from url
		try:
			FileName = str(counter) + str(fileFormat)
			print("Downloading from：" + url + ' To：' + FilePath)
			pic = requests.get(url, timeout=3).content
		except:
			print('Unable to fetch picture from url')
			continue
		# Write the file to the s
		try:
			file_obj = open(FilePath + FileName, 'wb')
			file_obj.write(pic)
			file_obj.close()
			print('img is downloaded!')
		except :
			print('Write File Failed')
		counter += 1
		if counter == amount:
			print('Stop for reaching target amount')
			return
	print('Stop. No More in list.')
	os.chdir(picDir)


if __name__ == "__main__":
	url_list = retriveUrl(keyWord='豪车',amount=500)
	retrivePic(raw_data=url_list,amount=len(url_list),dir='Good Car')

