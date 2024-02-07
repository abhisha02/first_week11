from django import forms
from .models import Account,UserProfile
from django.conf import settings
from twilio.rest import Client


class RegistrationForm(forms.ModelForm):

  password=forms.CharField(widget=forms.PasswordInput(attrs={
    'placeholder': 'Enter Password'
  }))
  confirm_password=forms.CharField(widget=forms.PasswordInput(attrs={
    'placeholder': 'Confirm Password'
  }))

  class Meta:
    model=Account
    fields=['first_name','last_name','phone_number','email','password']

  def __init__(self,*args,**kwargs):
    super(RegistrationForm,self).__init__(*args,**kwargs)
    self.fields['first_name'].widget.attrs['placeholder']='Enter First Name'
    self.fields['last_name'].widget.attrs['placeholder']='Enter Last Name'
    self.fields['phone_number'].widget.attrs['placeholder']='Enter Phone Number'
    self.fields['email'].widget.attrs['placeholder']='Enter Email Address'

    for field in self.fields:
      self.fields[field].widget.attrs['class']='form-control'

  def clean(self):
    cleaned_data= super(RegistrationForm,self).clean()
    password=cleaned_data.get('password')
    confirm_password=cleaned_data.get('confirm_password')

    if password!=confirm_password:
       raise forms.ValidationError(
           "Password does not match"
               )
    

class MessageHandler:
    phone_number=None
    otp=None
    def __init__(self,phone_number,otp) -> None:
        self.phone_number=phone_number
        self.otp=otp
    def send_otp_via_message(self):
        client= Client(settings.ACCOUNT_SID,settings.AUTH_TOKEN)
        message=client.messages.create(
                                body=f'your otp is:{self.otp}',
                                from_=f'{settings.TWILIO_PHONE_NUMBER}',
                                to=f'/{settings.COUNTRY_CODE}, {self.phone_number}'
                                )    
        

class UserForm(forms.ModelForm):
   
   profile_pic = forms.ImageField(
    required=False,
    error_messages={'invalid': {"Image Files only"}},
    widget=forms.FileInput
)

   
   class Meta:
      model=Account
      fields=['first_name','last_name','phone_number','profile_pic']


   def __init__(self,*args,**kwargs):
      super(UserForm,self).__init__(*args,**kwargs)

      for field in self.fields:
         self.fields[field].widget.attrs['class']='form-control'


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['address_line_1', 'address_line_2', 'city', 'state', 'country']

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
