from django.urls import path
from . import views

urlpatterns = [
	path('',views.home, name='freq'),
	path('result/', views.result, name='result')
]