from django import forms




class SimpleForm(forms.Form):
    def __init__(self, favorite_event_categories, *args, **kwargs):
        super(SimpleForm, self).__init__(*args, **kwargs)
        self.fields['favorite_event_categories'].choices = favorite_event_categories


    favorite_event_categories = forms.MultipleChoiceField(required=True,
        widget=forms.SelectMultiple(attrs={'size':'10', 'required':'True'}), choices=())
