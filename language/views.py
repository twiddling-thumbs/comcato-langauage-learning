from django.shortcuts import render, redirect
from django.contrib import messages
from authentication.models import Userdetail, Language, Payment, Material
from .form import ProfileForm
from json import dumps
from django.core.serializers.json import DjangoJSONEncoder
from django.contrib.auth.models import User
from django.core.mail import send_mail
from .form import ContactForm

def contact(request):
    if request.method == 'POST':
            form = ContactForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Your message was sent, thank you!')
                return redirect('contact')
    else:
            form = ContactForm()
            return render(request, 'contact.html', {'form': form})
# Create your views here.

def privacy(request):
    return render(request, 'privacy.html')


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
            return [[language.code,  language.name] for language in languages]

        else:
            return []
    except Language.DoesNotExist:
        return []


def get_payment_status(user_id):
    payments_Status = 0
    try:
        payments_Status = 1

    except Payment.DoesNotExist:
        # Handle the case when the Userdetails object does not exist for the user
        print('payments object does not exist for the user')
    return payments_Status


def get_all_audio_file(download):
    try:

        audiofiles_list = Material.objects.filter(type=download)
        if audiofiles_list:
            return [[audiofiles.file, audiofiles.name, get_language_id(audiofiles.your_language_id), get_language_id(audiofiles.foreign_language_id), str(audiofiles.file).split('.')[1]] for audiofiles in audiofiles_list]
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

    if request.user.is_authenticated:

        # Assuming 'languages' is the related_name in the Registration model
        user_language = get_user_languages(request.user.id)
        Language_list = []
        if (user_language != []):
            Language = user_language

            for code in Language:
                temp = []

                temp.append(get_langauge_name(code)[0])
                temp.append(code)
                Language_list.append(temp)

        Language_all = get_langauge_all()

        # Audio File
        # print(request.user.id)
        payments_Status = get_payment_status(request.user.id)
        download = 'free'
        if (payments_Status == 1):  # if payment is done
            download = 'premium'

        audio_list = get_all_audio_file(download)
        audio_dict = {}
        for data in audio_list:
            if data[2] not in audio_dict:
                audio_dict[data[2]] = []

            temp = [str(data[0]), data[1], data[4], data[2], data[3]]
            audio_dict[data[2]].append(temp)
        dataJSON = dumps(audio_dict, cls=DjangoJSONEncoder)
        context = {
            'data': dataJSON, 'title': 'Home', 'LANGUAGES': Language_list,
            'LANGUAGES_all': Language_all, 'audio_dict': audio_dict, 'download_status': download
        }
        return render(request, 'home.html', context)

    else:
        user_language = None

    # print(user_language)
    # languages = Language.objects.all()

    return render(request, 'home.html', {'title': 'Home'})


def articles(request):
    return render(request, 'articles.html', {'title': 'articles'})


def profile(request):

    if request.method == 'POST':
        existing_profile = None
        try:
            # Try to get the existing profile for the authenticated user
            existing_profile = Userdetail.objects.get(user=request.user.id)
            form = ProfileForm(request.POST, request.FILES)
            print('request.FILES')
            print(request.FILES)
            uploaded_file = request.FILES.get('file')
            print(uploaded_file)
        except Userdetail.DoesNotExist:
            # If the profile doesn't exist, create a new form
            form = ProfileForm(request.POST, request.FILES)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            address = form.cleaned_data['address']
            country = form.cleaned_data['country']
            gender = form.cleaned_data['gender']
            favouritetopic_values = form.cleaned_data['favouritetopic']
            your_language = form.cleaned_data['language']
            Interest_values = form.cleaned_data['Interest']
            # profile_picture = form.cleaned_data['profile_picture']

            if existing_profile is not None:
                user = User.objects.get(id=request.user.id)
                user.first_name = first_name
                user.last_name = last_name
                user.save()

                existing_profile.address = address
                existing_profile.country = country
                if gender == '1':
                    existing_profile.gender = 'M'
                elif gender == '2':
                    existing_profile.gender = 'F'
                existing_profile.profile_picture = profile_picture
                # print(country)
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
            # Assuming 'payment' is the name of the URL pattern for your payment page
            return redirect('profile')
        messages.error(request, 'Profile not Successfully updated.....')
        return redirect('profile')

    if request.user.is_authenticated:
        email = request.user.email
        firstname = ''
        lastname = ''
        gender = ''
        address = ''
        country = ''
        try:
            user_detail = Userdetail.objects.get(user=request.user.id)
            firstname = request.user.first_name if request.user.first_name is not None else ''
            lastname = request.user.last_name if request.user.last_name is not None else ''
            gender = user_detail.gender if user_detail.gender is not None else ''
            address = user_detail.address if user_detail.address is not None else ''
            country = user_detail.country if user_detail.country is not None else ''
            profile_picture = user_detail.profile_picture if user_detail.profile_picture is not None else ''

        except Userdetail.DoesNotExist:
            # Handle the case when the Userdetails object does not exist for the user
            print('Userdetails object does not exist for the user')

        payments_Status = get_payment_status(request.user)

        form = ProfileForm()

        return render(request, 'profile.html', {'title': 'profile', 'form': form, 'email': email,
                                                'firstname': firstname, 'lastname': lastname,
                                                'gender': gender, 'address': address, 'country': country,
                                                'payment': payments_Status})

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

    return render(request, 'payment.html', {'title': 'payments'})
