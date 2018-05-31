from django.shortcuts import render
import requests


def homepage(request):
	return render(request,'home.html')

def login(request):
	username = request.GET['username']
	password = request.GET['password']

	response = requests.get('http://freegeoip.net/json/')
	geodata = response.json()

	print(username, password)
	msg = "Successful login"
	return render(request,'show.html',{'message':msg,'ip': geodata['ip'],'country':geodata['country_name']})
