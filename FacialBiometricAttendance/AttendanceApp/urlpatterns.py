from django.urls import path
from . import views

urlpatterns = [
    path('',views.index, name = "index"), 
    path('attendance/',views.attendance, name = "attendance"), 
    path('faceid/',views.faceid, name = "faceid"), 
    path('result/',views.result, name = "result"), 
    path('record/',views.record, name = "record"), 
]
