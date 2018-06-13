from django.views.generic import View
from django.utils import timezone
from django.shortcuts import render
from .models import *
from .render import Render
from random import *
from decimal import Decimal


class Pdf(View):

	def get(self, request):
		articles = Articles.objects.all()
		today = timezone.now()
		print(today)
		params = {
       		'today': today,
        	'articles': articles,
    	}
		return Render.render('pdf.html', params)


"""class Seeder(View):

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
