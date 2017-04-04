from django import forms

class UserInfo(forms.Form):
	username = forms.CharField(label='username', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
	password = forms.CharField(label='password', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'password'}))

class SignupForm(forms.Form):
	username = forms.CharField(label='Username', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
	password = forms.CharField(label='Password', widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'password'}))
	password_repeat = forms.CharField(label="Retype Password", widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'password'}))
	first_name = forms.CharField(label='First Name', max_length=20, widget=forms.TextInput(attrs={'class': 'form-control'}))
	last_name = forms.CharField(label='Last Name', max_length=20, widget=forms.TextInput(attrs={'class': 'form-control'}))

	def clean(self):
		form_data = self.cleaned_data
		if form_data['password'] != form_data['password_repeat']:
			self._errors["password"] = ["Password do not match"]
			del form_data['password']
			del form_data['password_repeat']
		return form_data

Year_Choices=[(x, x) for x in range(1970, 2017)]
TF=[(True, True), (False, False)]

class listingForm(forms.Form):
	car_color = forms.CharField(label='color', widget=forms.TextInput(attrs={'class': 'form-control'}))
	car_make = forms.CharField(label='Car Make', widget=forms.TextInput(attrs={'class': 'form-control'}))
	car_model = forms.CharField(label='Car Model', widget=forms.TextInput(attrs={'class': 'form-control'}))
	car_year = forms.IntegerField(label='Year', widget=forms.Select(choices=Year_Choices))
	car_body_type = forms.CharField(label='Body Type', widget=forms.TextInput(attrs={'class': 'form-control'}))
	car_new = forms.BooleanField(label='This is a new car', widget=forms.Select(choices=TF))
	description = forms.CharField(label='Briefly Describe your car', widget=forms.Textarea)
	price = forms.IntegerField(label='Price Listing')
