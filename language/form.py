from django import forms
from authentication.models import Userdetail,Language,Interest,Favouritetopic,Contact


class ProfileForm(forms.Form):

    class Meta:
        model = Userdetail
        fields = ['first_name', 'last_name', 'email', 'address', 'country', 'gender', 'profile_picture']
    first_name = forms.CharField(label='First Name', max_length=100, required=True)
    last_name = forms.CharField(label='Last Name', max_length=100, required=True)
    email = forms.EmailField(label='Email', required=True)
    address = forms.CharField(label='Address', max_length=255, required=True)
    country = forms.CharField(label='Country', max_length=100, required=True)
    gender = forms.ChoiceField(label='Gender', choices=[('1', 'Male'), ('2', 'Female')], required=True)
    # profile_picture = forms.FileField(label='', required=False   , 
    #                        widget=forms.FileInput(attrs={'class': 'upload'}),)
    profile_picture = forms.FileField(
        label='',
        widget=forms.FileInput(attrs={'class': 'upload'}),
        required=True,
    )

   
    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        self.fields['language'] = forms.MultipleChoiceField(
            choices=self.get_language_choices(),
            widget=forms.SelectMultiple(attrs={'class': 'label ui selection fluid dropdown'})
        )

        self.fields['Interest'] = forms.MultipleChoiceField(
            choices=self.get_Interest_choices(),
            widget=forms.SelectMultiple(attrs={'class': 'label ui selection fluid dropdown'})
        )

        self.fields['favouritetopic'] = forms.MultipleChoiceField(
            choices=self.get_favouritetopic_choices(),
            widget=forms.SelectMultiple(attrs={'class': 'label ui selection fluid dropdown'})
        )

    def get_language_choices(self):
        languages = Language.objects.values_list('id', 'name')
        return languages
    
   

    def get_Interest_choices(self):
        interest = Interest.objects.values_list('id', 'title')
        return interest
    
    def get_favouritetopic_choices(self):
        favouritetopic = Favouritetopic.objects.values_list('id', 'title')
        return favouritetopic
    
    
    # logo = forms.FileField(label='Logo')
    # Add more fields as needed

    # You can also add widgets or validation as necessary
class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'subject': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Subject'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Write your message', 'rows': 7}),
        }