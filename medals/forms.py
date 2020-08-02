from django.forms import ModelForm
from .models import Medals

class MedalsForm(ModelForm):
    class Meta:
        model = Medals
        fields = ['title', 'memo', 'important', 'year', 'country', 'person']
