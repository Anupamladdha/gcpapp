from django import forms
from django.core.exceptions import ValidationError

import datetime

class PlacesForm(forms.Form):
    numberofdays=forms.IntegerField(required=True)
    place1 = forms.BooleanField(required=False)
    place2 = forms.BooleanField(required=False)
    place3 = forms.BooleanField(required=False)
    place4 = forms.BooleanField(required=False)
    place5 = forms.BooleanField(required=False)
    place6 = forms.BooleanField(required=False)
    place7 = forms.BooleanField(required=False)
    place8 = forms.BooleanField(required=False)
    place9 = forms.BooleanField(required=False)
    place10 = forms.BooleanField(required=False)
    place11 = forms.BooleanField(required=False)
    place12 = forms.BooleanField(required=False)
    place13 = forms.BooleanField(required=False)
    place14 = forms.BooleanField(required=False)
    place15 = forms.BooleanField(required=False)
    place16 = forms.BooleanField(required=False)
    place17 = forms.BooleanField(required=False)
    place18 = forms.BooleanField(required=False)
    place19 = forms.BooleanField(required=False)
    place20 = forms.BooleanField(required=False)
    place21 = forms.BooleanField(required=False)

class AvailabilityForm(forms.Form):
    check_in=forms.DateField(required=True,input_formats=["%Y-%m-%d"])
    check_out=forms.DateField(required=True,input_formats=["%Y-%m-%d"])
