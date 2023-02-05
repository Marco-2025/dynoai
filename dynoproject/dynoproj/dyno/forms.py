from django import forms
from .models import ImageUpload

class ImgForm(forms.ModelForm):
    class Meta:
        model = ImageUpload
        fields = {'id', 'image'}