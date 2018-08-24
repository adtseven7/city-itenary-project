from django.forms import ModelForm
from .models import *
from django import forms
import datetime
import floppyforms




class IteneraryForm(ModelForm):
	class Meta:
		model = Form
		fields = ['city','start_date','end_date','type_tags']
		widgets = {
			# 'city': floppyforms.widgets.Input(datalist=City.objects.all()),
	      	'type_tags':forms.CheckboxSelectMultiple,
	    	'start_date': forms.DateInput(attrs={'class':'datepicker', 'autocomplete': 'off'}),
	    	'end_date': forms.DateInput(attrs={'class':'datepicker', 'autocomplete': 'off'})
	    }

	def clean(self):
		cleaned_data = super(IteneraryForm, self).clean()
		start_date = cleaned_data.get("start_date")
		today_date = datetime.date.today()
		end_date = cleaned_data.get("end_date")

		if start_date and end_date:
			if start_date<today_date:
				raise forms.ValidationError("the start date is too early")
			if end_date<today_date:
				raise forms.ValidationError("the end date is too early")

			if start_date>end_date:
				raise forms.ValidationError("The start date cannot be after end date")

		# if end_date<today_date:
		# 	raise forms.ValidationError("the end date is too early")

		# if start_date > end_date:
		# 	raise forms.ValidationError("the end date can't be before start date")