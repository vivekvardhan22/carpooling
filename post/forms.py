from django import forms
from post.models import Post, Tag

class NewPostForm(forms.ModelForm):
    content = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'textarea', 'placeholder': 'What you are looking for and Write about any extra details'}),
        required=True
    )
    leaving_from = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'input is-medium', 'placeholder': 'Where are you leaving from?'}),
        required=True
    )
    going_to = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'input is-medium', 'placeholder': 'Where are you going to?'}),
        required=True
    )

    # Date and Time field with the TextInput widget
    date_time = forms.DateTimeField(
        widget=forms.DateTimeInput(
            attrs={
                'class': 'input is-medium',
                'type': 'datetime-local',  # Changed to datetime-local
                'placeholder': 'Pick a date and time'
            }
        ),
        required=True
    )

    # Transport Mode choices
    TRANSPORT_MODES = [
        ('car', 'Car'),
        ('flight', 'Flight'),
        ('train', 'Train'),
        ('bus', 'Bus'),
    ]
    transport_mode = forms.ChoiceField(
        choices=TRANSPORT_MODES,
        widget=forms.Select(attrs={'class': 'input is-medium'}),
        required=True
    )

    tags = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'input is-medium'}),
        required=True
    )

    class Meta:
        model = Post
        fields = ('content', 'leaving_from', 'going_to', 'date_time', 'transport_mode', 'tags')

    def __init__(self, *args, **kwargs):
        super(NewPostForm, self).__init__(*args, **kwargs)
        self.fields['tags'].widget.attrs.update({'class': 'checkbox'})
        self.fields['content'].widget.attrs.update({'class': 'textarea is-medium', 'rows': 4})

class SearchForm(forms.Form):
    leaving_from = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'input is-medium', 'placeholder': 'Where are you leaving from?'}),
        required=False
    )
    going_to = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'input is-medium', 'placeholder': 'Where are you going to?'}),
        required=False
    )
    date_time = forms.DateTimeField(
        widget=forms.DateTimeInput(
            attrs={
                'class': 'input is-medium',
                'type': 'datetime-local',
                'placeholder': 'Pick a date and time'
            }
        ),
        required=False
    )
