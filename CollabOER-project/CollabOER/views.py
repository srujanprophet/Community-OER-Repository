from django.shortcuts import render
import requests


def homepage(request):
	return render(request,'home.html')

def login(request):
	email = request.GET['email']
	password = request.GET['password']
	#curl -v -X POST --data "email=admin@dspace.org&password=mypass" https://dspace.myu.edu/rest/login
	url = 'http://127.0.0.1/rest/login'
	data = {'email':email, 'password':password}
	
	r = requests.post(url,data=data)
	print(r.text)
	comms = [{'name':'lol'},{'name':'fadfads'}]

	msg = "Successful login"
	return render(request,'show.html',{'message':msg,'comm':comms})
