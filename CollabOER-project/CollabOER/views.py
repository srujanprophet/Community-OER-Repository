from django.shortcuts import render

def homepage(request):
	return render(request,'home.html')

def login(request):
	username = request.GET['username']
	password = request.GET['password']

	print(username, password)
	msg = "Successful login"
	return render(request,'show.html',{'message':msg})