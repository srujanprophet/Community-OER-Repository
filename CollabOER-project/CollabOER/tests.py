from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse
from django.urls import resolve
from .views import homepage, get_communities, get_community_articles, get_groups, get_group_articles, login, logout, create_community, create_collection, create_groups,  create_community_resources, create_group_resources, create_group_bitstream, get_grouparticle_pdf, create_bitstream, getpdf

class HomeTestCase(TestCase):
	def test_homepage_view_status_code(self):
		url =reverse('homepage')
		response= self.client.get(url)
		self.assertEquals(response.status_code, 200)
	def test_homepage_url_resolves_homepage(self):
		view = resolve('/')
		self.assertEquals(view.func, homepage)

class CreateCommunityTestCase(TestCase):
	def test_create_community_view_status_code(self):
		url =reverse('createCommunity')
		response= self.client.get(url)
		self.assertEquals(response.status_code, 200)
	def test_create_community_url_resolves_create_community(self):
		view = resolve('/')
		self.assertTrue(view.func, create_community)

class CreateGroupTestCase(TestCase):
	def test_create_groups_view_status_code(self):
		url =reverse('createGroup')
		response= self.client.get(url)
		self.assertEquals(response.status_code, 200)
	def test_create_groups_url_resolves_create_groups(self):
		view = resolve('/')
		self.assertTrue(view.func, create_groups)
    
    
class CommunityresourcesTestCase(TestCase):
	def test_create_community_resources_view_status_code(self):
		url =reverse('createCommunityArticle')
		response= self.client.get(url)
		self.assertEquals(response.status_code, 200)
	def test_create_community_resources_url_resolves_create_community_resources(self):
		view = resolve('/')
		self.assertTrue(view.func, create_community_resources)


class GroupresourcesTestCase(TestCase):
	def test_create_group_resources_view_status_code(self):
		url =reverse('createGroupArticle')
		response= self.client.get(url)
		self.assertEquals(response.status_code, 200)
	def test_create_group_resources_url_resolves_create_group_resources(self):
		view = resolve('/')
		self.assertTrue(view.func, create_group_resources)
	
