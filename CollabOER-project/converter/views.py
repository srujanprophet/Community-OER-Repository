from django.views.generic import View
from django.utils import timezone
from django.shortcuts import render
from .models import *
from .render import Render
from random import *
from decimal import Decimal
import requests


class Pdf(View):

	def get(self, request):
		#articles = Articles.objects.all()
		url = 'http://127.0.0.1:8000/api/dspace/communityarticlesapi'  
		arti = requests.get(url)
		articles_list = arti.json()
		x = render(request,'index.html')
		#today = timezone.now()
		#print(today)
		incoming = 1
		i = 1
		
		for article in articles_list:
			year = article['created_at'][:4]
			month = article['created_at'][5:7]
			day = article['created_at'][8:10]
			hours = article['created_at'][11:13]
			minutes = article['created_at'][14:16]
			seconds = article['created_at'][17:19]
			date = day+"/"+month+"/"+year+" "+hours+":"+minutes+":"+seconds
			filename = "temp"+str(article['articleid'])+".pdf"
			params = {
				'title': article['title'],
				'body' : article['body'],
				'created_by': article['created_by'],
				'created_at': date,
				'cname': article['communityname'],
				}
			x = Render.render('pdf.html',params, filename, article['communityname'])
		return x


"""
class Seeder(View):

	def get(self, request):
		self.products = ["Mercurial Vapor", "Mercurial Superfly", "Hypervenom III", "Magista Obra", "Hypervenom Phantom", "Tiempo Legend"]
		for x in range(5):
			title = choice(self.products) + " {0}".format(randint(1, 10000))
			price = float(format(Decimal(str(random())), '.2f'))
			quantity = randint(1, 100)
			#customer = User.objects.get(pk=randint(1,3))
			product = Products(title=title, price=price)
			product.save()
			sale = Sales(product=product, quantity=quantity)
			sale.save()
			params = {'msg':'Done'}
		return render(request,'seeds.html',params)

"""
