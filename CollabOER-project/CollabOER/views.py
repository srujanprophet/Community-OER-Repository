from django.shortcuts import render

import requests


def homepage(request):
	return render(request,'home.html')

def login(request):

	#login api calling	
	url = 'http://127.0.0.1:80/rest/login'
	head = {'email': 'durgeshbarwal@gmail.com', 'password': '1773298936'}	
	r = requests.post(url, data=head)
	
	print(r.status_code)
	print(r.headers)
	


	#extracting  cookies
	s = r.headers['Set-Cookie']
	end = s.find(';')
	print(s[:end])

	k = (r.cookies['JSESSIONID'])
	print(k)
	
	#cookie vairable
	#cook = {'JSESSIONID': k}
	
	cookies = dict(JSESSIONID=k)
	
	#jar = requests.cookie.RequestsCookieJar()
	#jar.set('JSESSIONID', k)	
	
	

	#for posting an community through api
	url2 = 'http://127.0.0.1:80/rest/communities'
	#da2 = { 'name': 'Gymkhana', 'copyrightText': '', 'introductoryText': 'Welcome to the Sport Club', 'shortDescription': 'This', 'sidebarText': '' }
	da2 = { "name": "Gymkhana", "copyrightText": "", "introductoryText": "Welcome to the Sport Club", "shortDescription": "This", "sidebarText": "" }
	head2 = {'Content-Type': 'application/json'}
	r2 = requests.post(url2, headers=head2, data=da2, cookies={'JESSIONID': k})	
	
	print(r2.text)
	print(r2.headers)
	print(r2.url)
	print(r2.cookies)
		
	
	print(r2.status_code)
	msg = "Getting all the Communities in the System"
	return render(request,'show.html',{'message':msg})





