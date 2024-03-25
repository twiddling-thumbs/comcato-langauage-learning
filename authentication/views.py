from django.shortcuts import *
from .form import LoginForm,RegistrationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login as django_login , logout as django_logout
from .models import Userdetail
import uuid
from django.contrib.auth.models import User
from .utils import *
from django.contrib.sites.models import Site

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
           
            if user is not None:
                obj = Userdetail.objects.get(user = user.id)
                if(obj.is_verify):

                    django_login(request, user)
                    return redirect('home')  
                else:
                    messages.error(request, 'Account is not verify')
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
            # # Save the user to the database with the hashed password
            # # Create a RegistrationForm RegistrationForm
            userdetail_form_instance = Userdetail(
                user = user,
                email_token =str(uuid.uuid4())
            )
            userdetail_form_instance.save()

            a = send_email_token(email , userdetail_form_instance.email_token)
            messages.success(request, 'Registration successful. Please login.')
            # Perform necessary actions with the data
    Login_form = LoginForm()
    Register_form = RegistrationForm()
    return render(request,'login.html',{'title':'Login','Login_form':Login_form,'Register_form':Register_form,})

def logout(request):
    django_logout(request)
    return redirect('home')

def verify(request,token):
    try:
        

        obj = Userdetail.objects.get(email_token = token)
        obj.is_verify=True
        obj.save()
        return render(request,'verify.html',{'messages':'Your account is verify'})
    except Exception as e:
        return render(request,'verify.html',{'messages':'Your account is not verify'})