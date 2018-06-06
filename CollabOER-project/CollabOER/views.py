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
	# Authenticated Now
	# taking cookie

	k = (r.cookies['JSESSIONID'])
	print(k)
	#cookie variable
	cook = {'JSESSIONID': k}
	
	#url = 'http://127.0.0.1:80/rest/communities'
	
	#r2 = requests.post()	

	

	msg = "Getting all the Communities in the System"
	return render(request,'show.html',{'message':msg})

def test(request):
	sample = {
		"name":"FIFA WORLD CUP",
		"copyrightText":"",
		"introductoryText":"Welcome to Russia",
		"shortDescription":"Battle of the best.",
		"sidebarText":"",
		}
	url = 'http://127.0.0.1:80/rest/communities'
	option = 1
	if option == 0:
		cookie = {'JSESSIONID': '#Add your cookie'}

		r = requests.post(url,data=sample, cookies=cookie)

	if option == 1:
		cookies = {
			'JSESSIONID': '6B98CF8648BCE57DCD99689FE77CB1B8', #Add custom cookie
		}
		r = requests.post(url,json=sample, cookies=cookies)

	if option == 2:
		cookies = {
			'JSESSIONID': '6B98CF8648BCE57DCD99689FE77CB1B8', #Add custom cookie
		}
		headers = {
			'Content-Type': 'application/json',
		}

		r = requests.post(url,data=sample, cookies=cookies, headers=headers)

	if option == 3:
		jar = requests.cookies.RequestsCookieJar()
		jar.set('JSESSIONID', '6B98CF8648BCE57DCD99689FE77CB1B8', domain='127.0.0.1', path='/rest/communities')
		r = requests.post(url, json=sample, cookies=jar)
		print(r.text)

	print(r.status_code)
	return render(request,'post.html')

