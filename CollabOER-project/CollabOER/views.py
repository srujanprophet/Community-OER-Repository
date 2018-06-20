from django.shortcuts import render

import requests


def homepage(request):
	return render(request,'index.html')

def ccDashboard(request):
	return render(request,'CC.html')

def dspaceDashboard(request):
	return render(request, 'dspace.html')

def logindash(request):
	return render(request, 'login.html')

def login(request):

	url = 'http://127.0.0.1:80/rest/login'
	head = {'email': 'durgeshbarwal@gmail.com', 'password': '1773298936'}	
	r = requests.post(url, data=head)
	sessionid = r.cookies['JSESSIONID']
	if r.status_code==200:
		msg = "User Successfully Login to the System"
	else:
		msg = "Error in Login"	
	return render(request,'show.html',{'message':msg})

def logout(request):
	
	url = 'http://127.0.0.1:80/rest/logout'
	r = requests.post(url)
	if r.status_code==200:
		msg = "User Successfully Logout to the System"
	else:
		msg = "Error in Logout"	
	return render(request,'show.html',{'message':msg})

	

def create_community(request):

	url = 'http://127.0.0.1:80/rest/login'
	head = {'email': 'durgeshbarwal@gmail.com', 'password': '1773298936'}	
	r = requests.post(url, data=head)
	sessionid = r.cookies['JSESSIONID']
	if r.status_code==200:
		msg = "User Successfully Login to the System"
	else:
		msg = "Error in Login"	
	url = 'http://127.0.0.1:80/rest/communities'
	head = {'Content-Type': 'application/json'}
	data = { 
		"name": "FIFA World Cup",
		"copyrightText": "",
		"introductoryText": "Welcome to the Sport Club",
		"shortDescription": "This",
		"sidebarText": "" 
	}
	jar = requests.cookies.RequestsCookieJar()
	jar.set('JSESSIONID', sessionid, domain='127.0.0.1', path='/rest/communities')
	
	r = requests.post(url, headers=head, json=data, cookies = jar)
	if r.status_code==200:
		msg = "Community is Created"
	else: 
		msg = "Error in Community Creation"
	return render(request,'show.html',{'message':msg})


def create_sub_community(request):

	#Getting of all Communities
	url = 'http://127.0.0.1:80/rest/communities/top-communities'
	head = {'Content-Type': 'application/json'}
	r = requests.get(url, headers = head)
        
	#Getting the uuid of a community
	community_name = "Hello"
	uuid=-1
	for i in r.json():
		if community_name==i['name']:
			uuid=i['uuid']
			exit			
	#login 
	url = 'http://127.0.0.1:80/rest/login'
	head = {'email': 'durgeshbarwal@gmail.com', 'password': '1773298936'}	
	r = requests.post(url, data=head)
	sessionid = r.cookies['JSESSIONID']
	if r.status_code==200:
		msg = "User Successfully Login to the System"
	else:
		msg = "Error in Login"	
	
	#Creation of Sub Community
	url = 'http://127.0.0.1:80/rest/communities/' + uuid + '/communities'
	head = {'Content-Type': 'application/json'}
	data = { 
		"name": "FIFA World Cup",
		"copyrightText": "",
		"introductoryText": "Welcome to the Sport Club",
		"shortDescription": "This",
		"sidebarText": "" 
	}
	jar = requests.cookies.RequestsCookieJar()
	jar.set('JSESSIONID', sessionid, domain='127.0.0.1', path='/rest/communities')
	
	r = requests.post(url, headers=head, json=data, cookies = jar)
	if r.status_code==200:
		msg = "Sub-Community is Created"
	else: 
		msg = "Error in Sub- Community Creation"
		
	return render(request,'show.html',{'message':msg})


def create_collection(request):

	#Getting of all Communities
	url = 'http://127.0.0.1:80/rest/communities/top-communities'
	head = {'Content-Type': 'application/json'}
	r = requests.get(url, headers = head)
        
	#Getting the uuid of a community
	community_name = "Hello"
	uuid=-1
	for i in r.json():
		if community_name==i['name']:
			uuid=i['uuid']
			exit			
	#login 
	url = 'http://127.0.0.1:80/rest/login'
	head = {'email': 'durgeshbarwal@gmail.com', 'password': '1773298936'}	
	r = requests.post(url, data=head)
	sessionid = r.cookies['JSESSIONID']
	if r.status_code==200:
		msg = "User Successfully Login to the System"
	else:
		msg = "Error in Login"	
	

	#Creation of Sub Community
	url = 'http://127.0.0.1:80/rest/communities/' + uuid + '/collections'
	head = {'Content-Type': 'application/json'}
	data = { 
		"name": "A Collection",
		"copyrightText": "",
		"introductoryText": "Welcome to the Sport Club",
		"shortDescription": "This",
		"sidebarText": "" 
	}
	jar = requests.cookies.RequestsCookieJar()
	jar.set('JSESSIONID', sessionid, domain='127.0.0.1', path='/rest/communities')
	
	r = requests.post(url, headers=head, json=data, cookies = jar)
	if r.status_code==200:
		msg = "Collection is Created"
	else: 
		msg ="Error in Collection Creation"
		
	return render(request,'show.html',{'message':msg})


def insert_item(request):

	#Getting of all Collections
	url = 'http://127.0.0.1:80/rest/collections'
	head = {'Content-Type': 'application/json'}
	r = requests.get(url, headers = head)
        
	#Getting the uuid of a collection
	collection_name = "A Collection"
	uuid=-1
	for i in r.json():
		if collection_name==i['name']:
			uuid=i['uuid']
			exit			
	#login 
	url = 'http://127.0.0.1:80/rest/login'
	head = {'email': 'durgeshbarwal@gmail.com', 'password': '1773298936'}	
	r = requests.post(url, data=head)
	sessionid = r.cookies['JSESSIONID']
	if r.status_code==200:
		msg = "User Successfully Login to the System"
	else:
		msg = "Error in Login"	

	
	#Addition of an item in a collection
	url = 'http://127.0.0.1:80/rest/collections/' + uuid + '/items'
	head = {'Content-Type': 'application/json'}
	item = {
		"metadata":[
			{
			"key": "dc.contributor.author",
			"value": "Sinha, Hariom"
			},
			{
			"key": "dc.description",
			"language": "pt_BR",
			"value": "This article is usefull for the Sports team."
			},
			{
			"key": "dc.description.abstract",
			"language": "pt_BR",
			"value": "Another thing to note is that there are Query Parameters that you can tack on to the end of an endpoint to do extra things. The most commonly used one in this API. Instead of every API call defaulting to giving you every possible piece of information about it, it only gives a most commonly used set by default and gives the more information when you deliberately request it."
			},
			{
			"key": "dc.title",
			"language": "pt_BR",
			"value": "Basics of VollyBall"
			},
			{
			"key": "dc.date.issued",
			"value": "2018-05-03",
			"language": "en_US"
			},
			{
			"key": "dc.publisher",
			"value": "Mad Hostel",
			"language": "en_US"
			}
		]
	}
	jar = requests.cookies.RequestsCookieJar()
	jar.set('JSESSIONID', sessionid, domain='127.0.0.1', path='/rest/collections')
	
	r = requests.post(url, headers=head, json=item, cookies = jar)
	if r.status_code==200:
		msg = "Item is Inserted"
	else: 
		msg = "Error in Item Insertion"
		
	return render(request,'show.html',{'message':msg})



def insert_bitstream(request):

	
	#Getting of all Items
	url = 'http://127.0.0.1:80/rest/items'
	head = {'Content-Type': 'application/json'}
	r = requests.get(url, headers = head)
        

	#Getting the uuid of a Item
	item_name = "Basics of VollyBall"
	uuid=-1
	for i in r.json():
		if item_name==i['name']:
			uuid=i['uuid']
			exit			
	#login 
	url = 'http://127.0.0.1:80/rest/login'
	head = {'email': 'durgeshbarwal@gmail.com', 'password': '1773298936'}	
	r = requests.post(url, data=head)
	sessionid = r.cookies['JSESSIONID']
	if r.status_code==200:
		msg = "User Successfully Login to the System"
	else:
		msg = "Error in Login"	
	
	#Addition of an Bitstream in a item
	url = 'http://127.0.0.1:80/rest/items/' + uuid + '/bitstreams'
	head = {'Content-Type': 'application/json'}
	data = {"name": "5th_presentation.pdf", "description": "good"}
	
	jar = requests.cookies.RequestsCookieJar()
	jar.set('JSESSIONID', sessionid, domain='127.0.0.1', path='/rest/items')
	files = {'file': open('/home/dspace/Downloads/Project05_Presentation_04_2018_06_01.pdf', 'rb')}

	r = requests.post(url, files=files, headers=head, params=data, cookies = jar)
	print(r.url)	
	if r.status_code==200:
		msg = "File is Inserted"
	else: 
		msg = "Error in Item Insertion" + ": Error Code " + r.status_code
		
	return render(request,'show.html',{'message':msg})


