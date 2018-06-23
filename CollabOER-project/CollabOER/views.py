from django.shortcuts import render
from django.views.generic import View
from django.utils import timezone
from converter.render import Render
from random import *
from decimal import Decimal

import requests


def homepage(request):
	return render(request,'index.html')

def ccDashboard(request):
	return render(request,'CC.html')

def dspaceDashboard(request):
	return render(request, 'dspace.html')

def logindash(request):
	return render(request, 'login.html')

############# CC DASHBOARD ###############

def get_communities(request):
	r = requests.get('http://localhost:8000/api/dspace/communityapi/')
	data = r.json()	
	names = []
	for item in data:
		names.append(item['name'])

	if (r.status_code==200 and data):	
		message = 'Successfully Fetched all Communities from Collaboration System'
		return data
	elif r.status_code==200:
		message =  'No Communities to Fetch from Collaboration System Today'
		return 0
	else:
		message = 'Error in Fetching the Communities from Collaboration System'
		return 0
	

def get_community_articles(request):
	r = requests.get('http://localhost:8000/api/dspace/communityarticlesapi/')
	data = r.json()
	names = []
	for item in data:
		names.append(item['title'])

	if (r.status_code==200 and data):	
		message = 'Successfully Fetched all Resources of Communities from Collaboration System'
		return data
	elif r.status_code==200:
		message = 'No Resources to Fetch from Collaboration System'
		return 0
	else: 		
		message = 'Error in Fetching the Resources of Communities from Collaboration System'
		return 0
	
	#params = {'data': names, 'msg': message}
	#return render(request,'ccredirect.html',params)



def get_groups(request):
	r = requests.get('http://localhost:8000/api/dspace/groupapi/')	
	data = r.json()
	names = []
	for item in data:
		names.append(item['name'])

	if (r.status_code==200  and data):	
		message = 'Successfully Fetched all Groups of Communities from Collaboration System'
		return data
	elif r.status_code==200:
		message = 'No Groups to Fetch from Collaboration System'
		return 0
	else:
		message = 'Error in Fetching Groups of Communities from Collaboration System'
		return 0
	#params = {'data': names, 'msg': message }
	#return render(request,'ccredirect.html', params)

def get_group_articles(request):
	r = requests.get('http://localhost:8000/api/dspace/grouparticlesapi/')	
	data = r.json()
	names = []
	for item in data:
		names.append(item['title'])

	if (r.status_code==200 and data):	
		message = 'Successfully Fetched all Resources of Group from Collaboration System'
		return data
	elif r.status_code==200:
		message = 'No Resources of Group to Fetch from Collaboration System'
		return 0
	else:
		message = 'Error in Fetching Groups Resources of Group from Collaboration System'
		return 0
	
	#params = {'data': names, 'msg': message }
	#return render(request,'ccredirect.html', params)


################### AUTHENTICATION #######################

def login(request):

	url = 'http://127.0.0.1:80/rest/login'
	head = {'email': 'durgeshbarwal@gmail.com', 'password': '1773298936'}	
	r = requests.post(url, data=head)
	sessionid = r.cookies['JSESSIONID']
	if r.status_code==200:
		message = 'User Successfully Logged in to the DSpace System'
	else:
		message = 'Error in Login to DSpace System'
		return 500
	return sessionid
	
def logout(request):
	url = 'http://127.0.0.1:80/rest/logout'
	r = requests.post(url)
	if r.status_code==200:
		message = 'User Successfully Logged out from the DSpace System.'
		return 1
	else:
		message = 'Error in Logout from DSpace System'
		return 0

############### DSPACE DASHBOARD ###########################

def create_collection(request, collection, community, jar, k):
	#Getting of all Communities
	if k==0:	
		url = 'http://127.0.0.1:80/rest/communities/top-communities'
	else:
		url = 'http://127.0.0.1:80/rest/communities'		
	r = requests.get(url, headers = {'Content-Type': 'application/json'})
        
	#Getting the uuid of a community
	community_name = collection
	for i in r.json():
		if community_name==i['name']:
			uuid=i['uuid']
			exit			
	
	#Creation of Collection
	url = 'http://127.0.0.1:80/rest/communities/' + uuid + '/collections'
	head = {'Content-Type': 'application/json'}
		
	r = requests.post(url, headers=head, json=community, cookies = jar)
	if r.status_code==200:
		message = (request, 'Collection is Created Successfully in DSpace')
	else: 
		message = (request, 'Error in Collection Creation in DSpace')




def create_community(request):        
	#login funcion calling
	sessionid = login(request)
	names = []
	message = 'Communities Created : \n'

	if sessionid != 500:
		#User Successfully Login to the System
		#Community POST
		url = 'http://127.0.0.1:80/rest/communities'
		head = {'Content-Type': 'application/json'}
		jar = requests.cookies.RequestsCookieJar()
		jar.set('JSESSIONID', sessionid, domain='127.0.0.1', path='/rest/communities')
		k=100
		#Getting all the Communities from CC
		data = get_communities(request)

		if data != 0:
			for item in data:
				names.append(item['name'])

			for name in data:
				while(k==100):
					community={"name": name['name'],"copyrightText": "","introductoryText": "","shortDescription": name['desc'],"sidebarText": ""}
					r = requests.post(url, headers=head, json=community, cookies = jar)
					if r.status_code==200:
						message += 'Community is Created Successfully in DSpace'
						create_collection(request,name['name'],community,jar,0)        
						k=200
					else: 
						k=100				
						message = 'Error in Community Creation'
				k=100			
			#logout
			logout(request)

		else:
			message = 'No new communities were created yesterday.'

	params = {'msg': message, 'data': names }
	return render(request,'page2.html', params)


def create_groups(request):
	data = get_groups(request)
	message = 'Groups Created : \n'
	names = []
	
	if data!=0:
		for item in data:
			names.append(item['name'])
		#login funcion calling
		sessionid = login(request)
		if sessionid != 500:
			#Getting of all Communities
			url = 'http://127.0.0.1:80/rest/communities/top-communities'
			r = requests.get(url, headers = {'Content-Type': 'application/json'})
			for group in data:
				#Getting the uuid of a community
				community_name = group['communityname'] #*****************
				for i in r.json():
					if community_name==i['name']:
						uuid=i['uuid']
						exit
				if uuid:
					url = 'http://127.0.0.1:80/rest/communities/' + uuid + '/communities'
					jar = requests.cookies.RequestsCookieJar()
					jar.set('JSESSIONID', sessionid, domain='127.0.0.1', path='/rest/communities')
					content={ "name": group['name'], "copyrightText": "", "introductoryText": "Welcome to the Sport Club", "shortDescription": "This", "sidebarText": ""}
					r = requests.post(url, headers={'Content-Type': 'application/json'}, json = content, cookies = jar)				#*********
					if r.status_code==200:
						message += 'Group is Created in DSpace'
						#**************
						create_collection(request,group['name'],content,jar,1)
					else: 
						message = 'Error in Group Creation in DSpace'
		if sessionid != 500:
			#logout
			logout(request)

	else:
		message = 'No new groups were created yesterday'
	
	params = {'msg': message , 'data': names}
	return render(request,'page3.html', params)

def create_community_resources(request):
	data = get_community_articles(request)
	names = []
	message = 'Community Articles Created : \n'
	
	if data!=0: 
		for item in data:
			names.append(item['title'])
		#login funcion calling
		sessionid = login(request)
		if sessionid != 500:
			#Getting of all Collections
			url = 'http://127.0.0.1:80/rest/collections'
			r = requests.get(url, headers = {'Content-Type': 'application/json'})
			for name in data:			        
				#Getting the uuid of a collection
				collection_name = name['communityname']
				for i in r.json():
					if collection_name == i['name']:
						uuid=i['uuid']
						exit
				#Addition of an item in a collection
				if uuid != 0:	
					url = 'http://127.0.0.1:80/rest/collections/' + uuid + '/items'
					item = {"metadata":[
							{
							"key": "dc.contributor.author",
							"value": name['created_by']
							},
							{
							"key": "dc.title",
							"language": "pt_BR",
							"value": name['title']
							},
							{
							"key": "dc.date.issued",
							"value": name['published_on'],
							"language": "en_US"
							},
							{
							"key": "dc.publisher",
							"value": "Collaboration System",
							"language": "en_US"
							}]}
					jar = requests.cookies.RequestsCookieJar()
					jar.set('JSESSIONID', sessionid, domain='127.0.0.1', path='/rest/collections')
					r = requests.post(url, headers={'Content-Type': 'application/json'}, json=item, cookies = jar)
					if r.status_code==200:
						message += 'Item is Created Successfully in DSpace'
						create_bitstream(request, name['title'], name, sessionid)
					else: 
						message = 'Error in Item and File POSTing to DSpace'
		if sessionid!=500:
			#logout
			logout(request)

	else:
		msg = 'No new Community Articles were created yesterday'	
	
	params = {'msg': message, 'data': names }
	return render(request,'page4.html', params)



def create_group_resources(request):
	data = get_group_articles(request)
	message = 'Group Articles Created : \n'
	names = []
	
	if data!=0: 
		for item in data:
			names.append(item['title'])
		#login funcion calling
		sessionid = login(request)
		if sessionid != 500:
			#Getting of all Collections
			url = 'http://127.0.0.1:80/rest/collections'
			r = requests.get(url, headers = {'Content-Type': 'application/json'})
			for name in data:			        
				#Getting the uuid of a collection
				collection_name = name['groupname']
				for i in r.json():
					if collection_name == i['name']:
						uuid=i['uuid']
						exit
				#Addition of an item in a collection
				if uuid != 0:	
					url = 'http://127.0.0.1:80/rest/collections/' + uuid + '/items'
					item = {"metadata":[
							{
							"key": "dc.contributor.author",
							"value": name['created_by']
							},
							{
							"key": "dc.title",
							"language": "pt_BR",
							"value": name['title']
							},
							{
							"key": "dc.date.issued",
							"value": name['published_on'],
							"language": "en_US"
							},
							{
							"key": "dc.publisher",
							"value": "Collaboration System",
							"language": "en_US"
							}]}
					jar = requests.cookies.RequestsCookieJar()
					jar.set('JSESSIONID', sessionid, domain='127.0.0.1', path='/rest/collections')
					r = requests.post(url, headers={'Content-Type': 'application/json'}, json=item, cookies = jar)
					if r.status_code==200:
						message += 'Item is Created Successfully in DSpace'
						create_group_bitstream(request, name['title'], name, sessionid)
					else: 
						message += 'Error in Item and File POSTing to DSpace'
		if sessionid!=500:
			#logout
			logout(request)	
	else:
		msg = 'No New Group Articles were published yesterday.'


	params = {'msg': message, 'data': names }
	return render(request,'epilogue.html', params)


def create_group_bitstream(request, title, name, sessionid):	
	
	#Getting of all Items
	url = 'http://127.0.0.1:80/rest/items'
	r = requests.get(url, headers={'Content-Type': 'application/json'})
        
	
	#Getting the uuid of a Item
	item_name=title
	for i in r.json():
		if (item_name and i['name']):
			uuid=i['uuid']
			exit

	#Addition of an Bitstream in a item
	url = 'http://127.0.0.1:80/rest/items/' + uuid + '/bitstreams'
	filename = str(name['groupname']) + str(name['articleid']) + '.pdf'	
	data = {"name": filename, "description": ""}
	
	jar = requests.cookies.RequestsCookieJar()
	jar.set('JSESSIONID', sessionid, domain='127.0.0.1', path='/rest/items')
				
	temp = get_grouparticle_pdf(request, name)
	files = {'file': open('Files/group'+ str(name['articleid']) +'.pdf', 'rb')}
	
	r = requests.post(url, files=files, headers={'Content-Type': 'application/json'}, params=data, cookies = jar)
	if r.status_code==200:
		message = 'File is Inserted Successfully'
	else: 
		message = 'Error in File Insertion Creation'


def get_grouparticle_pdf(request, name):
		
		filename = "group"+str(name['articleid'])+".pdf"
		params = {
			'title': name['title'],
			'body' : name['body'],
			'created_by': name['created_by'],
			'cname': name['groupname'],
			'published_on' : name['published_on']
			}
	
		x = Render.render('group_pdf.html',params, filename, name['groupname'])
		return x

def create_bitstream(request, title, name, sessionid):	
	
	#Getting of all Items
	url = 'http://127.0.0.1:80/rest/items'
	r = requests.get(url, headers={'Content-Type': 'application/json'})
        
	
	#Getting the uuid of a Item
	item_name=title
	for i in r.json():
		if (item_name and i['name']):
			uuid=i['uuid']
			exit

	#Addition of an Bitstream in a item
	url = 'http://127.0.0.1:80/rest/items/' + uuid + '/bitstreams'
	filename = str(name['communityname']) + str(name['articleid']) + '.pdf'	
	data = {"name": filename, "description": ""}
	
	jar = requests.cookies.RequestsCookieJar()
	jar.set('JSESSIONID', sessionid, domain='127.0.0.1', path='/rest/items')
				
	temp = getpdf(request, name)
	files = {'file': open('communities/temp'+ str(name['articleid']) +'.pdf', 'rb')}
	
	r = requests.post(url, files=files, headers={'Content-Type': 'application/json'}, params=data, cookies = jar)
	if r.status_code==200:
		message = 'File is Inserted Successfully'
	else: 
		message = 'Error in File Insertion Creation'


def getpdf(request, name):
		
	filename = "temp"+str(name['articleid'])+".pdf"
	params = {
		'title': name['title'],
		'body' : name['body'],
		'created_by': name['created_by'],
		'cname': name['communityname'],
		'published_on' : name['published_on']
		}

	x = Render.render('pdf.html',params, filename, name['communityname'])
	return x