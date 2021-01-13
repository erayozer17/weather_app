from django import forms

from .models import City


class CityForm(forms.ModelForm):

    class Meta:
        model = City
        fields = ('name',)

    def clean_name(self):
        name = self.cleaned_data['name']
        return name.strip()
