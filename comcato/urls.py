from django.urls import path
from . import views


# url configuartion
urlpatterns = [
    path('',views.home,name='home'),
    path('profile/',views.profile,name='profile'),
    path('payments/',views.Userpayments,name='payments'),
    path('Userpayments/',views.Userpayments_add,name='Userpayments'),
    path('articles/',views.articles,name='articles'),
   
]