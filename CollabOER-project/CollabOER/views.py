from django.shortcuts import render
from django.contrib import messages

import requests


def homepage(request):
	return render(request,'home.html')

def test_get_communities(request):
	r = requests.get('http://localhost:8000/communityapi/')
	
	data = r.json()
	if data:	
		print(data)
	else: 
		print('error')
	
	for name in data:
		print(name['name'])
		
	if r.status_code==200:	
		messages.success(request, 'Successfully Fetch all Communities')
	else:
		messages.error(request, 'Error in Fetching the Communities')	
	return render(request,'home.html',{'data':data})

def get_communities(request):
	r = requests.get('http://localhost:8000/communityapi/')
	
	data = r.json()
	print(data)
	for name in data:
		print(name['name'])
		
	if r.status_code==200:	
		messages.success(request, 'Successfully Fetch all Communities')
		return data
	else:
		messages.error(request, 'Error in Fetching the Communities')
		return 0


def get_community_resources(request):
	r = requests.get('http://localhost:8000/api/communityarticlesapi/')
	
	data = r.json()
	print(data)
	for name in data:
		print(name['title'])
		
	if r.status_code==200:	
		messages.success(request, 'Successfully Fetch all Communities')
	else:
		messages.error(request, 'Error in Fetching the Communities')
	return render(request,'home.html',{'data1':data})


def get_groups(request):
	messages.success(request, 'Successfully Fetch all Groups')
	return render(request,'home.html')

def get_group_resources(request):
	messages.success(request, 'Successfully Fetch all Group Resources')
	return render(request,'home.html')



def login(request):

	url = 'http://127.0.0.1:80/rest/login'
	head = {'email': 'durgeshbarwal@gmail.com', 'password': '1773298936'}	
	r = requests.post(url, data=head)
	sessionid = r.cookies['JSESSIONID']
	if r.status_code==200:
		messages.success(request, 'User Successfully Login to the System')
		return sessionid
	else:
		messages.error(request, 'Error in Login')
		return 500

def test_login(request):

	url = 'http://127.0.0.1:80/rest/login'
	head = {'email': 'durgeshbarwal@gmail.com', 'password': '1773298936'}	
	r = requests.post(url, data=head)
	sessionid = r.cookies['JSESSIONID']
	if r.status_code==200:
		messages.success(request, 'User Successfully Login to the System')
	else:
		messages.error(request, 'Error in Login')	
	return render(request,'home.html')


def logout(request):
	url = 'http://127.0.0.1:80/rest/logout'
	r = requests.post(url)
	if r.status_code==200:
		messages.success(request, 'User Successfully Logout to the System.')
		return 1
	else:
		message.error(request, 'Error in Logout')
		return 0
	
def test_logout(request):
	url = 'http://127.0.0.1:80/rest/logout'
	r = requests.post(url)
	if r.status_code==200:
		messages.success(request, 'User Successfully Logout to the System.')
	else:
		message.error(request, 'Error in Logout')
	
	return render(request,'home.html')

def create_community(request):
        
	#login
	sessionid = login(request)
	if sessionid == 500:
		messages.error(request, 'Error in Login')
	else:
		messages.success(request, 'User Successfully Login to the System')	
	#Community POST
	
	url = 'http://127.0.0.1:80/rest/communities'
	head = {'Content-Type': 'application/json'}

	jar = requests.cookies.RequestsCookieJar()
	jar.set('JSESSIONID', sessionid, domain='127.0.0.1', path='/rest/communities')
	
	k=100
	data=get_communities(request)
	for name in data:
		while(k==100):
			community={"name": name['name'],"copyrightText": "","introductoryText": "","shortDescription": name['desc'],"sidebarText": ""}
			r = requests.post(url, headers=head, json=community, cookies = jar)
			if r.status_code==200:
				messages.success(request, 'Community is Created Successfully')
				create_collection(request,name['name'],community,jar)


        
				k=200
			else: 
				k=100				
				messages.error(request, 'Error in Community Creation')
		k=100
	
	#logout
	logout(request)
	return render(request,'home.html')

def create_collection(request, collection, community, jar):

	#Getting of all Communities
	url = 'http://127.0.0.1:80/rest/communities/top-communities'
	r = requests.get(url, headers = {'Content-Type': 'application/json'})
        
	#Getting the uuid of a community
	community_name = collection
	for i in r.json():
		if community_name==i['name']:
			uuid=i['uuid']
			exit			
	
	#Creation of Sub Community
	url = 'http://127.0.0.1:80/rest/communities/' + uuid + '/collections'
	head = {'Content-Type': 'application/json'}
		
	r = requests.post(url, headers=head, json=community, cookies = jar)
	if r.status_code==200:
		messages.success(request, 'Collection is Created Successfully')
	else: 
		messages.error(request, 'Error in Collection Creation')



def test_create_collection(request):

	#Getting of all Communities
	url = 'http://127.0.0.1:80/rest/communities/top-communities'
	head = {'Content-Type': 'application/json'}
	r = requests.get(url, headers = head)
        
	#Getting the uuid of a community
	community_name = "Hello"
	uuid=0
	for i in r.json():
		if community_name==i['name']:
			uuid=i['uuid']
			exit			
	#login
	sessionid = test_login(request)
	if sessionid == 500:
		messages.error(request, 'Error in Login')
	else:
		messages.success(request, 'User Successfully Login to the System')	
	
	#Creation of Sub Community
	if uuid!=0:
		url = 'http://127.0.0.1:80/rest/communities/' + uuid + '/collections'
		head = {'Content-Type': 'application/json'}
		data = { 
		"name": "A Collection",
		"copyrightText": "",
		"introductoryText": "Welcome to the Sport Club",
		"shortDescription": "This",
		"sidebarText": ""}
		jar = requests.cookies.RequestsCookieJar()
		jar.set('JSESSIONID', sessionid, domain='127.0.0.1', path='/rest/communities')
	
		r = requests.post(url, headers=head, json=data, cookies = jar)
		if r.status_code==200:
			messages.success(request, 'Collection is Created Successfully')
		else: 
			messages.error(request, 'Error in Collection Creation')
	else:
		messages.error(request,'Top Level Community Not Found')
	#logout
	logout(request)
	return render(request,'home.html')



def create_sub_community(request):
	#Getting of all Communities
	url = 'http://127.0.0.1:80/rest/communities/top-communities'
	head = {'Content-Type': 'application/json'}
	r = requests.get(url, headers = head)
        
	#Getting the uuid of a community
	community_name = "Hello"
	uuid=0
	for i in r.json():
		if community_name==i['name']:
			uuid=i['uuid']
			exit			

	#login
	sessionid = login(request)
	if sessionid == 500:
		messages.error(request, 'Error in Login')
	else:
		messages.success(request, 'User Successfully Login to the System')	

	#Creation of Sub Community
	if uuid != 0:	
		url = 'http://127.0.0.1:80/rest/communities/' + uuid + '/communities'
		head = {'Content-Type': 'application/json'}
		jar = requests.cookies.RequestsCookieJar()
		jar.set('JSESSIONID', sessionid, domain='127.0.0.1', path='/rest/communities')
		r = requests.post(url, headers=head, json={ 
		"name": "FIFA World Cup",
		"copyrightText": "",
		"introductoryText": "Welcome to the Sport Club",
		"shortDescription": "This",
		"sidebarText": ""}, cookies = jar)
		if r.status_code==200:
			messages.success(request, 'Sub-Community is Created Successfully')
		else: 
			messages.error(request, 'Error in Sub-Community Creation')
	else:
		messages.error(request, 'Top Level Community Not Found')
	
	#logout	
	logout(request)
	return render(request,'home.html')


def insert_item(request):

	#Getting of all Collections
	url = 'http://127.0.0.1:80/rest/collections'
	head = {'Content-Type': 'application/json'}
	r = requests.get(url, headers = head)
        
	#Getting the uuid of a collection
	collection_name = "A Collection"
	uuid=0
	for i in r.json():
		if collection_name==i['name']:
			uuid=i['uuid']
			exit			
	#login
	sessionid = test_login(request)
	if sessionid == 500:
		messages.error(request, 'Error in Login')
	else:
		messages.success(request, 'User Successfully Login to the System')	
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
		messages.success(request, 'Item is Created Successfully')
	else: 
		messages.error(request, 'Error in Item Creation')	
	#logout
	logout(request)		
	return render(request,'home.html')

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
	sessionid = test_login(request)
	if sessionid == 500:
		messages.error(request, 'Error in Login')
	else:
		messages.success(request, 'User Successfully Login to the System')	

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
		messages.success(request, 'File is Inserted Successfully')
	else: 
		messages.error(request, 'Error in File Insertion Creation')
	
	#logout
	logout(request)		
	return render(request,'home.html')


