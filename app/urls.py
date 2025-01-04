from django.urls import path
from .views import intro_video
from django.conf.urls.static import static
from django.conf import settings
from . import views 


urlpatterns = [
    path('', views.intro_video, name='intro_video'),
    path('home/', views.home, name='home'), 
    path('graphical/', views.graphical, name='graphical'),
    path('simplex/', views.simplex, name='simplex'),  
 
] 
