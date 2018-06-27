from django.shortcuts import render
from django.views.generic import View
from django.utils import timezone
from converter.render import Render
from random import *
from decimal import Decimal

import requests


def homepage(request):
	return render(request,'index.html')


############# CC DASHBOARD ###############

def get_communities(request):
	r = requests.get('http://localhost:8000/api/dspace/communityapi/')
	data = r.json()	

	if (r.status_code==200 and data):	
		message = 'Successfully Fetched all Communities from Collaboration System'
		return data,message
	elif r.status_code==200:
		message =  'No Communities to Fetch from Collaboration System Today'
		return [],message
	else:
		message = 'Error in Fetching the Communities from Collaboration System'
		return [],message
	

def get_community_articles(request):
	r = requests.get('http://localhost:8000/api/dspace/communityarticlesapi/')
	data = r.json()
	

	if (r.status_code==200 and data):	
		message = 'Successfully Fetched all Resources of Communities from Collaboration System'
		return data, message
	elif r.status_code==200:
		message = 'No Resources to Fetch from Collaboration System'
		return [],message
	else: 		
		message = 'Error in Fetching the Resources of Communities from Collaboration System'
		return [],message
	
	#params = {'data': names, 'msg': message}
	#return render(request,'ccredirect.html',params)



def get_groups(request):
	r = requests.get('http://localhost:8000/api/dspace/groupapi/')	
	data = r.json()

	if (r.status_code==200  and data):	
		message = 'Successfully Fetched all Groups of Communities from Collaboration System'
		return data, message
	elif r.status_code==200:
		message = 'No Groups to Fetch from Collaboration System'
		return [],message
	else:
		message = 'Error in Fetching Groups of Communities from Collaboration System'
		return [],message

	#params = {'data': names, 'msg': message }
	#return render(request,'ccredirect.html', params)

def get_group_articles(request):
	r = requests.get('http://localhost:8000/api/dspace/grouparticlesapi/')	
	data = r.json()

	if (r.status_code==200 and data):	
		message = 'Successfully Fetched all Resources of Group from Collaboration System'
		return data, message
	elif r.status_code==200:
		message = 'No Resources of Group to Fetch from Collaboration System'
		return [],message
	else:
		message = 'Error in Fetching Groups Resources of Group from Collaboration System'
		return [],message
	
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
	# Getting all Communities
	if k==0:	
		url = 'http://127.0.0.1:80/rest/communities/top-communities'
	else:
		url = 'http://127.0.0.1:80/rest/communities'		
	r = requests.get(url, headers = {'Content-Type': 'application/json'})
        
	# Getting the uuid of a community
	community_name = collection
	for i in r.json():
		if community_name == i['name']:
			uuid=i['uuid']
			exit			
	# Creating Collection
	url = 'http://127.0.0.1:80/rest/communities/' + uuid + '/collections'
	head = {'Content-Type': 'application/json'}
		
	r = requests.post(url, headers=head, json=community, cookies = jar)
	if r.status_code==200:
		return 1
	else: 
		return 0




def create_community(request):        
	# logging in
	sessionid = login(request)
	names = []
	# message = 'No New Communities \n'
	data, message = get_communities(request)

	if sessionid != 500:
		# User Successfully Logged into the System
		# Community POST
		url = 'http://127.0.0.1:80/rest/communities'
		head = {'Content-Type': 'application/json'}
		jar = requests.cookies.RequestsCookieJar()
		jar.set('JSESSIONID', sessionid, domain='127.0.0.1', path='/rest/communities')
		k=100
		# Getting all the Communities from CC
		count=0
		count_community=0;count_collection=0
		
		if data != 0:
			for item in data:
				names.append(item['name'])
				count=count+1
			for name in data:
				community={"name": name['name'],"copyrightText": "","introductoryText": "","shortDescription": name['desc'],"sidebarText": ""}
				r = requests.post(url, headers=head, json=community, cookies = jar)
				if r.status_code==200:
					count_community = count_community + 1
					flag = create_collection(request,name['name'],community,jar,0)        
					count_collection = count_collection + flag
				else: 				
					message = 'Error in Community Creation'	
			if count_community == count_collection == count:
				success_flag=1
			else: 
				success_flag=0				
		else:
			message = 'No new communities were created yesterday.'
			success_flag=1
	params = {'msg': message, 'data': names,'success_flag': success_flag }
	return render(request,'community_article.html', params)


def create_groups(request):
	data, message = get_groups(request)
	#message = 'Groups Created : \n'
	names = []
	success_flag=0

	if data!=0:
		for item in data:
			names.append(item['name'])
		# logging in
		sessionid = login(request)
		if sessionid != 500:
			# Getting all Communities
			url = 'http://127.0.0.1:80/rest/communities/top-communities'
			r = requests.get(url, headers = {'Content-Type': 'application/json'})
			count=0
			count_community=0;count_collection=0
			for group in data:
				count=count+1
				# Getting the uuid of a community
				cname = group['community_name'] 
				for i in r.json():
					if cname == i['name']:
						uuid=i['uuid']
						exit
				
				url = 'http://127.0.0.1:80/rest/communities/' + uuid + '/communities'
				jar = requests.cookies.RequestsCookieJar()
				jar.set('JSESSIONID', sessionid, domain='127.0.0.1', path='/rest/communities')
				content={ "name": group['name'], "copyrightText": "", "introductoryText": "Welcome to the Sport Club", "shortDescription": "This", "sidebarText": ""}
				req = requests.post(url, headers={'Content-Type': 'application/json'}, json = content, cookies = jar)		
				if req.status_code==200:
					count_community = count_community + 1
					message = 'Group is Created in DSpace'
					flag=create_collection(request,group['name'],content,jar,1)
					count_collection = count_collection + flag
				else: 
					message = 'Error in Group Creation in DSpace'
			if count_community == count_collection:
				success_flag=1
			else: 
				success_flag=0
		else:
			success_flag=0		
		if sessionid != 500:
			# logging out
			logout(request)

	else:
		message = 'No new groups were created yesterday'
		success_flag=1
	
	params = {'msg': message, 'data': names,'success_flag': success_flag }
	return render(request,'group.html', params)

def create_community_resources(request):
	data, message = get_community_articles(request)
	names = []
	#message = 'Community Articles Created : \n'	

	if data!=0: 
		for item in data:
			names.append(item['title'])
		# logging in 
		sessionid = login(request)
		if sessionid != 500:
			# Getting all Collections
			url = 'http://127.0.0.1:80/rest/collections'
			r = requests.get(url, headers = {'Content-Type': 'application/json'})
			count=0
			count_item=0;count_bitstream=0
			
			for name in data:
				count=count+1
				
				#Getting the uuid of a collection
				collection_name = name['communityname']
				for i in r.json():
					if collection_name == i['name']:
						uuid=i['uuid']
						exit
				# Addition of an item to a collection
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
				req = requests.post(url, headers={'Content-Type': 'application/json'}, json=item, cookies = jar)
				if req.status_code==200:
					message = 'Item is Created Successfully in DSpace'
					count_item = count_item + 1
					flag = create_bitstream(request, name['title'], name, sessionid)
					count_bitstream = count_bitstream + flag
				else: 
					message = 'Error in Item and File POSTing to DSpace'
			if count_item == count_bitstream:
				success_flag=1
			else: 
				success_flag=0		
		else:
			success_flag=0		
		if sessionid!=500:
			# logging out
			logout(request)

	else:
		message = 'No new Community Articles were created yesterday'	
		success_flag=1
	params = {'msg': message, 'data': names,'success_flag': success_flag }
	return render(request,'group_article.html', params)



def create_group_resources(request):
	data, message = get_group_articles(request)
	#message = 'Group Articles Created : \n'
	names = []
				
	

	if data!=0: 
		for item in data:
			names.append(item['title'])
			
		# logging in
		sessionid = login(request)
		if sessionid != 500:
			# Getting all Collections
			url = 'http://127.0.0.1:80/rest/collections'
			r = requests.get(url, headers = {'Content-Type': 'application/json'})
			count=0
			count_item=0;count_bitstream=0
			
			for name in data:			        
				count=count+1
				
				# Getting the uuid of a collection
				collection_name = name['groupname']
				for i in r.json():
					if collection_name == i['name']:
						uuid=i['uuid']
						exit
				# Addition of an item to a collection
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
					req = requests.post(url, headers={'Content-Type': 'application/json'}, json=item, cookies = jar)
					if req.status_code==200:
						message = 'Item is Created Successfully in DSpace'
						count_item = count_item + 1
						flag = create_group_bitstream(request, name['title'], name, sessionid)
						count_bitstream = count_bitstream + flag
						
					else: 
						message = 'Error in Item and File POSTing to DSpace'
			if count_item == count_bitstream:
				success_flag=1
			else: 
				success_flag=0		
		else:
			success_flag=0				
		if sessionid!=500:
			# logging out
			logout(request)	
	else:
		message = 'No New Group Articles were published yesterday.'
		success_flag = 1

	params = {'msg': message, 'data': names,'success_flag': success_flag }
	return render(request,'epilogue.html', params)


def create_group_bitstream(request, title, name, sessionid):	
	
	# Getting all Items
	url = 'http://127.0.0.1:80/rest/items'
	r = requests.get(url, headers={'Content-Type': 'application/json'})
        
	# Getting the uuid of a Item
	item_name=title
	for i in r.json():
		if (item_name == i['name']):
			uuid=i['uuid']
			exit
	# Addition of a Bitstream to an item
	url = 'http://127.0.0.1:80/rest/items/' + uuid + '/bitstreams'
	filename = str(name['groupname']) + str(name['articleid']) + '.pdf'	
	data = {"name": filename, "description": ""}
	
	jar = requests.cookies.RequestsCookieJar()
	jar.set('JSESSIONID', sessionid, domain='127.0.0.1', path='/rest/items')
				
	temp = get_grouparticle_pdf(request, name)
	files = {'file': open('cache/group'+ str(name['articleid']) +'.pdf', 'rb')}
	
	req = requests.post(url, files=files, headers={'Content-Type': 'application/json'}, params=data, cookies = jar)
	if req.status_code==200:
		return 1
	else: 
		return 0


def get_grouparticle_pdf(request, name):
	year = name['created_at'][:4]
	month = name['created_at'][5:7]
	day = name['created_at'][8:10]
	hours = name['created_at'][11:13]
	minutes = name['created_at'][14:16]
	seconds = name['created_at'][17:19]
	date = day+"/"+month+"/"+year+" "+hours+":"+minutes+":"+seconds

	filename = "group"+str(name['articleid'])+".pdf"
	params = {
			'title': name['title'],
			'body' : name['body'],
			'created_by': name['created_by'],
			'cname': name['groupname'],
			'published_on' : name['published_on'],
			'created_at': date
		}
	
	x = Render.render('group_pdf.html',params, filename, name['groupname'])
	return x

def create_bitstream(request, title, name, sessionid):	
	
	# Getting of all Items
	url = 'http://127.0.0.1:80/rest/items'
	r = requests.get(url, headers={'Content-Type': 'application/json'})
        
	# Getting the uuid of an Item
	item_name=title
	for i in r.json():
		if item_name == i['name']:
			uuid=i['uuid']
			exit

	# Addition of a Bitstream to an item
	url = 'http://127.0.0.1:80/rest/items/' + uuid + '/bitstreams'
	filename = str(name['communityname']) + str(name['articleid']) + '.pdf'	
	data = {"name": filename, "description": ""}
	
	jar = requests.cookies.RequestsCookieJar()
	jar.set('JSESSIONID', sessionid, domain='127.0.0.1', path='/rest/items')
				
	temp = getpdf(request, name)
	files = {'file': open('cache/community'+ str(name['articleid']) +'.pdf', 'rb')}
	
	req = requests.post(url, files=files, headers={'Content-Type': 'application/json'}, params=data, cookies = jar)
	if req.status_code==200:
		return 1
	else: 
		return 0


def getpdf(request, name):
	year = name['created_at'][:4]
	month = name['created_at'][5:7]
	day = name['created_at'][8:10]
	hours = name['created_at'][11:13]
	minutes = name['created_at'][14:16]
	seconds = name['created_at'][17:19]
	date = day+"/"+month+"/"+year+" "+hours+":"+minutes+":"+seconds

	filename = "community"+str(name['articleid'])+".pdf"
	params = {
		'title': name['title'],
		'body' : name['body'],
		'created_by': name['created_by'],
		'cname': name['communityname'],
		'published_on' : name['published_on'],
		'created_at': date
		}

	x = Render.render('pdf.html',params, filename, name['communityname'])
	return x