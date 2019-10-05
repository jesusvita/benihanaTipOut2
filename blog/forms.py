from django.forms import ModelForm
from .models import tipOut

class personalTeppan(ModelForm):
    class Meta:
        model = tipOut
        fields = ['teppan', 'sushi', 'bar', 'tip']
