from django import forms

class UserInfo(forms.Form):
	username = forms.CharField(label='username', max_length=100)
	password = forms.CharField(label='password', max_length=100)

class SignupForm(forms.Form):
	username = forms.CharField(label='Username', max_length=100)
	password = forms.CharField(label='Password', widget=forms.PasswordInput)
	password_repeat = forms.CharField(label="Retype Password",widget=forms.PasswordInput)
	first_name = forms.CharField(label='First Name', max_length=20)
	last_name = forms.CharField(label='Last Name', max_length=20)

	def clean(self):
		form_data = self.cleaned_data
		if form_data['password'] != form_data['password_repeat']:
			self._errors["password"] = ["Password do not match"]
			del form_data['password']
			del form_data['password_repeat']
		return form_data
