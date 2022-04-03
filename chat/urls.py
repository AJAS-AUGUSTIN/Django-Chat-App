from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('<str:username>',views.chatPage, name='chat'),
    path('login/',views.login, name = 'login'),
    path('logout/',views.logout,name='logout'),
]