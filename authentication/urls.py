from django.urls import path
from . import views


# url configuartion
urlpatterns = [
    path('',views.login,name='login'),
    path('account/<str:token>',views.verify),
    path('register/',views.add_user,name='Sign Up'),
    path('login/',views.login_validation,name='Sign In'),
    path('logout/', views.logout, name='logout'),
   
]