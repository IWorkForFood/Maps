from django import forms

class MarkerForm(forms.Form):
    """
    The form for memories/impressions creation
    """

    places_name = forms.CharField(label='Название места', max_length=40, required=True)
    about_place = forms.CharField(widget=forms.Textarea(
        attrs={'rows': 10, 'cols': 80, 'class': 'about-place', 'placeholder': 'Поделитесь мыслями об этом месте'}),
        label='О месте', required=False)
    x_location = forms.FloatField()
    y_location = forms.FloatField()

    def __str__(self):
        return self.places_name