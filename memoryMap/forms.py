from django import forms

class MarkerForm(forms.Form):

    places_name = forms.CharField(label='Название места', required=True)
    about_place = forms.CharField(widget=forms.Textarea(
        attrs={'rows': 10, 'cols': 80, 'class': 'about-place', 'placeholder': 'Расскажите об этом месте'}), required=False)
    x_location = forms.FloatField()
    y_location = forms.FloatField()