from django.shortcuts import render
import requests


def homepage(request):
	return render(request,'home.html')

def login(request):
	email = request.GET['email']
	password = request.GET['password']
	#curl -v -X POST --data "email=admin@dspace.org&password=mypass" https://dspace.myu.edu/rest/login
	url = 'http://127.0.0.1:80/rest/communities'
	#params = {'email': email, 'password': password}
	#response = requests.get('http://freegeoip.net/json/')
	#geodata = response.json()
	#r = requests.post(url, params=params)
	r = requests.get(url)
	temp = r[0]['name']
	msg = "Successful login"
	return render(request,'show.html',{'message':msg,'comm':temp})
