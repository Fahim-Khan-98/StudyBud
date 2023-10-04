from django.urls import path
from . import views

urlpatterns = [
    path('',views.home, name="home"),
    path('room/<str:pk>/',views.room, name="room"),
    path('user-profile/<str:pk>/',views.UserProfile, name="user-profile"),
    path('update-user/',views.UpdateUser, name="update-user"),

    path('create-room/',views.CreateRoom, name="create-room"),
    path('update-room/<str:pk>/',views.UpdateRoom, name="update-room"),
    path('delete-room/<str:pk>/',views.DeleteRoom, name="delete-room"),
    path('delete-message/<str:pk>/',views.DeleteMessage, name="delete-message"),


    path('topic/',views.TopicPage, name="topics"),
    path('activity/',views.ActivityPage, name="activity"),


     


    # Authentication
    path('register/',views.RegisterPage, name="register"),
    path('login/',views.LoginPage, name="login"),
    path('logout/',views.LogoutUser, name="logout"),

]