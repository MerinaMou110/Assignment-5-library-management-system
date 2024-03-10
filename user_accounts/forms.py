from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from . models import UserAccount
from .constants import  GENDER_TYPE
from django.contrib.auth.forms import PasswordChangeForm


class UserRegistrationForm(UserCreationForm):
    birth_date = forms.DateField(widget=forms.DateInput(attrs={'type':'date'}))
    gender = forms.ChoiceField(choices=GENDER_TYPE)
    street_address = forms.CharField(max_length=100)
    city = forms.CharField(max_length= 100)
    postal_code = forms.IntegerField()
    country = forms.CharField(max_length=100)
    phone_num = forms.CharField(max_length=15)
    
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'first_name', 'last_name', 'email','gender','phone_num', 'birth_date', 'postal_code', 'city','country', 'street_address']
        

     # form.save()
        #views.py a form save er shate jeno akshate 3 ta model er data save hoy shei kaj ta korbo
    def save(self, commit=True):
        #Call the save method of the parent class(usercreationform) to get the user instance
        # form a fillup kora user er data gulo our_user a cole ashbe
        our_user = super().save(commit=False) # ami database e data save korbo na ekhn
        if commit == True:
            our_user.save() # user model e data save korlam

            # Extract additional fields from the form's cleaned_data
            phone_num = self.cleaned_data.get('phone_num')
            gender = self.cleaned_data.get('gender')
            postal_code = self.cleaned_data.get('postal_code')
            country = self.cleaned_data.get('country')
            birth_date = self.cleaned_data.get('birth_date')
            city = self.cleaned_data.get('city')
            street_address = self.cleaned_data.get('street_address')
            
            # Create UserAccount instance and link it to the user
            UserAccount.objects.create(
                user = our_user,
                gender = gender,
                postal_code = postal_code,
                country = country,
                city = city,
                street_address = street_address,
                birth_date =birth_date,
                phone_num=phone_num,
                account_no = 100000+ our_user.id
            )

           
        # Return the user instance
        return our_user
    

# for form decoration
    #This is the constructor method for your form. It's called when an instance of the form is created.
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # fields er modhe shb ase like pass,bd,acc_type etc
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                
                'class' : (
                    'appearance-none block w-full bg-gray-200 '
                    'text-gray-700 border border-gray-200 rounded '
                    'py-3 px-4 leading-tight focus:outline-none '
                    'focus:bg-white focus:border-gray-500'
                ) 
            })



class UserUpdateForm(forms.ModelForm):
    birth_date = forms.DateField(widget=forms.DateInput(attrs={'type':'date'}))
    gender = forms.ChoiceField(choices=GENDER_TYPE)
    street_address = forms.CharField(max_length=100)
    city = forms.CharField(max_length= 100)
    postal_code = forms.IntegerField()
    country = forms.CharField(max_length=100)
    phone_num = forms.CharField(max_length=15)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': (
                    'appearance-none block w-full bg-gray-200 '
                    'text-gray-700 border border-gray-200 rounded '
                    'py-3 px-4 leading-tight focus:outline-none '
                    'focus:bg-white focus:border-gray-500'
                )
            })
        # jodi user er account thake 
        if self.instance:
            try:
                user_account = self.instance.account
                
            except UserAccount.DoesNotExist:
                user_account = None
                

            if user_account:
                
                self.fields['gender'].initial = user_account.gender
                self.fields['birth_date'].initial = user_account.birth_date
                self.fields['street_address'].initial = user_account.street_address
                self.fields['city'].initial = user_account.city
                self.fields['postal_code'].initial = user_account.postal_code
                self.fields['country'].initial = user_account.country
                self.fields['phone_num'].initial = user_account.phone_num

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()

            user_account, created = UserAccount.objects.get_or_create(user=user) # jodi account thake taile seta jabe user_account ar jodi account na thake taile create hobe ar seta created er moddhe jabe
           

            user_account.street_address = self.cleaned_data['street_address']
            user_account.city = self.cleaned_data['city']
            user_account.postal_code = self.cleaned_data['postal_code']
            user_account.country = self.cleaned_data['country']
            user_account.gender = self.cleaned_data['gender']
            user_account.birth_date = self.cleaned_data['birth_date']
            user_account.save()

            

        return user



class CustomPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': (
                    'appearance-none block w-full bg-gray-200 '
                    'text-gray-700 border border-gray-200 rounded '
                    'py-3 px-4 leading-tight focus:outline-none '
                    'focus:bg-white focus:border-gray-500'
                )
            })
