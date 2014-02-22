import requests

site = 'http://ctfteam5.mit.edu:3000'
user_data = {'username' : 'FooBarBaz', 'password' : 'HelloWorld', 'type' : 'teacher'}
#r = requests.post(site + '/login/',data=user_data)
r = requests.post(site + '/login/', data=user_data)
print r.text