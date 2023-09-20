from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile

class custom_user_creation_form(UserCreationForm):

  class Meta:
    model = User
    fields = ['username', 'email', 'password1', 'password2']
    # label = {
    #   'password1': 'Password',
    #   'password2': 'Confirm password',
    # }

  def __init__(self, *args, **kwargs):
    super(custom_user_creation_form, self).__init__(*args, **kwargs)

    self.fields['username'].widget.attrs['class'] = 'form_input'
    self.fields['username'].widget.attrs['placeholder'] = 'This name will not be public, Profile Name will be'
    self.fields['username'].widget.help_text = '<span class="form_help_text"><p>Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.</p></span>'

    self.fields['email'].widget.attrs['class'] = 'form_input'
    self.fields['email'].widget.attrs['placeholder'] = "example@email.com . This won't be public"
    self.fields['email'].widget.help_text = ''
    self.fields['email'].required = True

    self.fields['password1'].widget.attrs['class'] = 'form_input'
    # self.fields['password1'].widget.attrs['type'] = 'password'
    self.fields['password1'].widget.attrs['placeholder'] = '8 characters and not entirely numeric'
    self.fields['password1'].widget.help_text = '<ul class="form_help_text"><li>Your password can\'t be too similar to your other personal information.</li><li>Your password must contain at least 8 characters.</li><li>Your password can\'t be a commonly used password.</li><li>Your password can\'t be entirely numeric.</li></ul>'
    
    self.fields['password2'].widget.attrs['class'] = 'form_input'
    # self.fields['password2'].widget.attrs['type'] = 'password'
    self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'
    self.fields['password2'].widget.help_text = '<span class="form_help_text"><p>Enter the same password as before, for verification.</p></span>'
    
    
class profile_form(ModelForm):
  class Meta:
    model = Profile
    fields = ['username','name', 'email', 'profile_picture', 'bio', 'work', 'location', 
        'contact', 'social_website', 'facebook',
        'linkedin', 'twitter', 'you_tube'
      ]

  def __init__(self, *args, **kwargs):
    super(profile_form, self).__init__(*args, **kwargs)

    self.fields['username'].widget.attrs['placeholder'] = 'This name will not be public, Name will be'
    self.fields['name'].widget.attrs['placeholder'] = 'This name will be public'
    # self.fields['email'].widget.attrs['placeholder'] = ''
    # self.fields['bio'].widget.attrs['placeholder'] = 'let everyone know you'
    self.fields['contact'].widget.attrs['placeholder'] = "public email address, phone. your registration email won't be public"
    self.fields['social_website'].widget.attrs['placeholder'] = 'you can share your website'
    self.fields['facebook'].widget.attrs['placeholder'] = 'you can share your facebook link'
    self.fields['linkedin'].widget.attrs['placeholder'] = 'you can share your linkedin link'
    self.fields['twitter'].widget.attrs['placeholder'] = 'you can share your twitter link'
    self.fields['you_tube'].widget.attrs['placeholder'] = 'you can share your you_tube link'





