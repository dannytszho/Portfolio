"""Define URL patterns for d_portfolio."""

from django.urls import path

from . import views

from .views import Graph

app_name = "d_portfolio"
urlpatterns = [
	# Home page
	path('', views.index, name='index'),
	# COVID19 Page
	path('COVID19', Graph.as_view(), name='COVID19'),
	# DeFi page
	path('defi', views.defi, name='defi'),
]