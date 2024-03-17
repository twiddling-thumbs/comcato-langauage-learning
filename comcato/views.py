from django.shortcuts import *
import logging
import time
import shelve
from django.http import JsonResponse
from django.contrib import messages
import json
from authentication.models import Userdetail,Language,Payment,Material,Interest,Favouritetopic
from .form import ProfileForm
from json import dumps 
from django.core.serializers.json import DjangoJSONEncoder
from django.core.paginator import Paginator



# Create your views here.
def get_language_id(language_id):
    language = Language.objects.get(id=language_id)
    return language.code


def get_user_languages(user_id):
    try:
        userdetails = Userdetail.objects.get(user_id=user_id)
        # Assuming your_language is a ManyToManyField in the Userdetail model
        return userdetails.your_language.all()

    except Userdetail.DoesNotExist:
        return []
    

    
def get_langauge_all():
    try: 
        languages = Language.objects.all()
        if languages:
            return [[ language.code ,  language.name] for language in languages]

        else:
            return []  
    except Language.DoesNotExist:
        return []
    
def get_payment_status(user_id):
    payments_Status=0
    try:
        paymentsvalue = Payment.objects.get(user=user_id)
        payments_Status = 1

    except Payment.DoesNotExist:
        # Handle the case when the Userdetails object does not exist for the user
        print('payments object does not exist for the user')
    return payments_Status



def get_all_audio_file(download):
    try:
        
        audiofiles_list = Material.objects.filter(type=download)
        if audiofiles_list:
            return [[audiofiles.file ,audiofiles.name, get_language_id(audiofiles.your_language_id),get_language_id(audiofiles.foreign_language_id),str(audiofiles.file).split('.')[1]]  for audiofiles in audiofiles_list]
        else:
            return []  

    except Material.DoesNotExist:
        return []  

def get_langauge_name(code):
    try:
        
        languages = Language.objects.filter(name=code)
        if languages:
            return [language.code for language in languages]

        else:
            return []  

    except Language.DoesNotExist:
        return []

def home(request):
    print("home")

    if request.user.is_authenticated:

        user_language = get_user_languages(request.user.id)  # Assuming 'languages' is the related_name in the Registration model
        print('user_language')
        print(user_language)
        Language_list=[]
        if(user_language!=[]):
            Language = user_language
           
            for code in Language:
                temp=[]
                
                temp.append(get_langauge_name(code)[0])
                temp.append(code)
                Language_list.append(temp)
        
        print(Language_list)

        Language_all = get_langauge_all()

        # Audio File 
        # print(request.user.id)
        payments_Status = get_payment_status(request.user.id)
        download='free'
        if(payments_Status==1):  # if payment is done
            download='premium'
        
        audio_list  =  get_all_audio_file(download)
        print(download)
        print(audio_list)
        audio_dict = {}
        for data in audio_list:
            if data[2] not in audio_dict:
                audio_dict[data[2]] = []

            temp = [str(data[0]), data[1],data[4],data[2],data[3]]
            audio_dict[data[2]].append(temp)
        print('audio_dict')
        print(audio_dict)
        dataJSON = dumps(audio_dict, cls=DjangoJSONEncoder)
        return render(request,'home.html',{'data': dataJSON,'title':'Home','LANGUAGES':Language_list,'LANGUAGES_all':Language_all,'audio_dict':audio_dict,'download_status':download})
       

    else:
        user_language = None



    # print(user_language)
    # languages = Language.objects.all()
    
    return render(request,'home.html',{'title':'Home'})


def articles(request):
    print("articles")
    return render(request,'articles.html',{'title':'articles'})


def profile(request):
    print("profile")
    print(request.user.is_authenticated)
    print(request.user.id)
    if request.user.is_authenticated:

        user_data = Userdetail.objects.get(user=request.user.id)
        email = request.user.email
        firstname =''
        lastname =''
        gender =''
        address =''
        country =''
        try:
            user_detail = Userdetail.objects.get(user=request.user.id)
            firstname = user_detail.firstname if user_detail.firstname is not None else ''
            lastname = user_detail.lastname if user_detail.lastname is not None else ''
            gender = user_detail.Gender if user_detail.Gender is not None else ''
            address = user_detail.address if user_detail.address is not None else ''
            country = user_detail.Country if user_detail.Country is not None else ''

        except Userdetail.DoesNotExist:
            # Handle the case when the Userdetails object does not exist for the user
            print('Userdetails object does not exist for the user')

        payments_Status = get_payment_status(request.user)

        form = ProfileForm()

        return render(request,'profile.html',{'title':'profile','form':form,'email':email,
                                              'firstname':firstname,'lastname':lastname,
                                              'gender':gender,'address':address,'country':country,'payment':payments_Status})
    

    return redirect('home')


def Userpayments_add(request):
    print("Userpayments_add")

    payments_user = Payment(
            user=request.user,
            paymentsstatus=1      
    )
    payments_user.save()
    messages.success(request, 'Payment Successfully save.....')
    return redirect('profile')

def Userpayments(request):
    print("payments")

    return render(request,'payment.html',{'title':'payments'})

def add_Profile(request):
    print("update profile data")
    existing_profile=None
    try:
        # Try to get the existing profile for the authenticated user
        existing_profile = Userdetail.objects.get(user=request.user.id)
        form = ProfileForm(request.POST, request.FILES)
    except Userdetail.DoesNotExist:
        # If the profile doesn't exist, create a new form
        form = ProfileForm(request.POST, request.FILES)
    # form = ProfileForm(request.POST, request.FILES)
    print(form.is_valid())
    print(form.cleaned_data)
    if request.method == 'POST' and form.is_valid():
        # Process the form data
        # print(form.cleaned_data)
        first_name = form.cleaned_data['first_name']
        last_name = form.cleaned_data['last_name']
        email = form.cleaned_data['email']
        address = form.cleaned_data['address']
        country = form.cleaned_data['country']
        gender = form.cleaned_data['gender']
        favouritetopic_values = form.cleaned_data['favouritetopic']
        your_language = form.cleaned_data['language']
        Interest_values = form.cleaned_data['Interest']
        profile_picture = form.cleaned_data['profile_picture']

        # print(request.FILES)

        print(existing_profile)
        if existing_profile != None:
            print("update profile data")
            # Update the existing profile
            existing_profile.firstname = first_name
            existing_profile.lastname = last_name
            existing_profile.address = address
            existing_profile.Country = country
            if gender == '1':
                existing_profile.Gender = 'M'
            elif gender == '2':
                existing_profile.Gender = 'F'
            existing_profile.profile_picture = profile_picture
            existing_profile.save()

            # Favourite Topic
           
            
            # Clear existing favourite topics
            existing_profile.favourite_topics.clear()

            # Add new favourite topics
            for topic in favouritetopic_values:
                existing_profile.favourite_topics.add(topic)

            # Interest
            # Clear existing Interest topics
            existing_profile.interests.clear()

            # Add new favourite topics
            for interest in Interest_values:
                existing_profile.interests.add(interest)

            # languaage
            # Clear existing languaage topics
            existing_profile.your_language.clear()

            # Add new favourite topics
            for language in your_language:
                existing_profile.your_language.add(language)

        # Favourtie Topic
            
        
    
        messages.success(request, 'Profile Successfully updated.....')

        # Redirect to another page or return a response
        return redirect('profile')  # Assuming 'payment' is the name of the URL pattern for your payment page
    messages.success(request, 'Profile not Successfully updated.....')
    return redirect('profile')


