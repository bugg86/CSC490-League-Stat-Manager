from django import forms

class CreateSearchForm(forms.Form):
	name = forms.CharField(label="Search ", max_length=300)