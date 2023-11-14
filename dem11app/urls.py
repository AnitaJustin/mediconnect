# yourappname/urls.py
from django.urls import path
from .views import *

urlpatterns = [
    path("",homepage,name="homepage"),
    path('signup/', signup, name='signup'),
    path('signin/',signin, name='signin'),
    path('dashboard/',dashboard,name='dashboard'),
    path('medicine/',medicine,name='medicine'),
    path('aids/', aids, name='aids'),
    path('receiver/', receiver, name='receiver'),
    
]
