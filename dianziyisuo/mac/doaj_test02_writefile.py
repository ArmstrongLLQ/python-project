

# -*- coding: utf-8 -*-
import json
import requests
import urllib
import codecs

class DOAJ:
	def __init__(self, base_url, auth, filter):
		self.base_url = base_url
		self.auth = auth
		self.filter = filter

	def getBaseUrl(self):
		return self.base_url

	def setBaseUrl(self, new_base_url):
		self.base_url = new_base_url

	def getAuth(self):
		return self.auth

	def setAuth(self, new_auth):
		self.auth = new_auth

	def getFilter(self):
		return self.filter

	def setFilter(self, new_filter):
		self.filter = new_filter

	def test_get_doaj_list(self):
		rsp = requests.get(urllib.parse.urljoin(self.base_url, '/doaj/'), auth=self.auth, params=self.filter)
		rsp.encoding = 'utf-8'
		print(rsp)
		#json_temp = rsp.json()
		if rsp.ok:
			json_file = codecs.open('data6.json', 'a', 'utf-8')
			for each in rsp.json()['results']:
				# print(str(each) + '\n')
				json_file.write(str(each) + '\n')
			# with open('data5.json', 'a') as json_file:
			# 	for each in rsp.json()['results']:
			# 		json_file.write(str(each) + '\n')
				# json_file.write(str(rsp.json()['results'][0]['id']))
				print('success')
			#print(rsp.json())

if __name__ == '__main__':
	base_url = 'http://121.42.164.187:8088/'
	auth = ('xxjs', '123456a?')
	filter = {"term_l1":"Science","year":"2017"}

	test1 = DOAJ(base_url, auth, filter)
	test1.test_get_doaj_list()

