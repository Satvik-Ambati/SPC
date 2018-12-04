from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from db_file_storage.form_widgets import DBClearableFileInput


class UserRegisterForm(UserCreationForm):
	email = forms.EmailField()

	class Meta:
		model = User
		fields = ['username', 'email', 'password1', 'password2']

class UserLoginForm(forms.ModelForm):
	username=forms.CharField(max_length=50)
	password=forms.CharField(widget=forms.PasswordInput)
	class Meta:
		model = User
		fields = ['username', 'password']

# class UploadForm(forms.ModelForm):
# 	type_of_file = forms.CharField(max_length=50)
# 	file = forms

class DocumentForm(forms.Form):
	description = forms.CharField(max_length=100)
	document = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))
	class Meta:
		model = User
		# fields = ['description', 'document']
		exclude = ['uploaded_at','filename']
		widgets = {
			'document': DBClearableFileInput
		}
