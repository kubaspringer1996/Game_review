from django import forms
from .models import Review

class ReviewForm(forms.ModelForm):
	"""formulář pro přidávání recenzí"""
	RATING_CHOICES = [(i, str(i)) for i in range(1,11)]
	rating = forms.ChoiceField(choices=RATING_CHOICES)
	
	class Meta:
		model = Review
		fields = ['rating','text']
