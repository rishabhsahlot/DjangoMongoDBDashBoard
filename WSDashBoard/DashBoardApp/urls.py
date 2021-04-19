from django.conf.urls import url
from DashBoardApp import views

urlpatterns = [
    url(r'^api/DashBoardApp/APIs$', views.APIList),
    url(r'^api/DashBoardApp/Mashups$', views.MashupList)
]
