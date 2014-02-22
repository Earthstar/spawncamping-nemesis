import requests

user_data = {'username' : 'FooBarBaz', 'password' : 'HelloWorld', 'type' : 'teacher'}
for i in xrange(2,10):
	site = 'http://ctfteam' + str(i) + '.mit.edu:3000'
	#r = requests.post(site + '/login/',data=user_data)
	r = requests.post(site + '/login/', data=user_data)
	#print r.text