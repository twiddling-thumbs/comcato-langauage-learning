from django.shortcuts import *
from .form import LoginForm,RegistrationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login as django_login , logout as django_logout
from .models import Userdetail
from django.contrib.auth.models import User
# Create your views here.



def login(request):

    Login_form = LoginForm()
    Register_form = RegistrationForm()

    return render(request,'login.html',{'title':'Login','Login_form':Login_form,'Register_form':Register_form,})


def login_validation(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            # Authenticate user
            user = authenticate(request, username=username, password=password)
            print('user')
            print(user)
           
            if user is not None:
                django_login(request, user)
                return redirect('home')  
            else:
                messages.error(request, 'Invalid username or password.')
    Login_form = LoginForm()
    Register_form = RegistrationForm()
    return render(request,'login.html',{'title':'Login','Login_form':Login_form,'Register_form':Register_form,})

def add_user(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
           
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
          


            if User.objects.filter(email=email).exists():
                messages.error(request, 'Email address is already in use.')
                return redirect('login')
            
            if User.objects.filter(username=username).exists():
                messages.error(request, 'UserName address is already in use.')
                return redirect('login')
            
           
            user = User.objects.create_user(username, email,password)
            # user.save()

            # # Save the user to the database with the hashed password
            # # Create a RegistrationForm RegistrationForm
            userdetail_form_instance = Userdetail(
                user = user,
            )
            userdetail_form_instance.save()


            # # Set the ManyToManyField using set()
            # registration_form_instance.languages.set(languages)

            messages.success(request, 'Registration successful. Please login.')
            # Perform necessary actions with the data
    Login_form = LoginForm()
    Register_form = RegistrationForm()
    return render(request,'login.html',{'title':'Login','Login_form':Login_form,'Register_form':Register_form,})

def logout(request):
    django_logout(request)
    return redirect('home')