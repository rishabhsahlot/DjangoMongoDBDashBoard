from django.conf.urls import url
from DashBoardApp import views

urlpatterns = [
    url(r'^api/DashBoardApp/APIs$', views.APIList),
    url(r'^api/DashBoardApp/Mashups$', views.MashupList),
    url(r'^api/DashBoardApp/Counts$', views.getCounts),
    url(r'^api/DashBoardApp/DeleteAPIs$', views.deleteAPIs),
    url(r'^api/DashBoardApp/DeleteMashups$', views.deleteMashups)
]
