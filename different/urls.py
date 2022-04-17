from django.urls import path
from . import views

urlpatterns = [
    path("" , views.index , name="index") ,
    path("activities" , views.random_activities , name="random") , 
    path("bucket_list" , views.bucket_list , name="bucket_list") , 
    path('completed/<str:item>' , views.completed , name="completed"),
    path("calendar" , views.random_events , name="calendar") , 
    path('connect' , views.connect , name="connect") ,
    path('share' , views.share_completed , name="share"),
    path("login" , views.login_view , name="login") , 
    path("register" , views.register , name="register")  ,
    path("logout" , views.logout_view , name="logout") , 

    path('not-found/<str:message>' , views.error , name='error')
]