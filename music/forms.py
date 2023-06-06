from django import forms
from .models import Audio


class AudioForm(forms.ModelForm):
    """ A form that uploads new audio song to db """

    class Meta:
        """ Select Audio model and pick all the form fields in db """
        model = Audio
        fields = '__all__'
