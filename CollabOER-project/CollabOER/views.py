from django.shortcuts import render

import requests


def homepage(request):
	return render(request,'home.html')

def login(request):
	url = 'http://127.0.0.1:80/rest/login'
	head = {'email': 'durgeshbarwal@gmail.com', 'password': '1773298936'}	
	r = requests.post(url, data=head)
	
	print(r.status_code)
	print(r.headers)
	
	#taking cookie
	s = r.headers['Set-Cookie']
	end = s.find(';')
	print(s[:end])

	k = (r.cookies['JSESSIONID'])
	print(k)
	print(k)
	#cookie vairable
	cook = {'JSESSIONID': k}
	
	#url = 'http://127.0.0.1:80/rest/communities'
	
	#r2 = requests.post()	

	

	msg = "Getting all the Communities in the System"
	return render(request,'show.html',{'message':msg})

