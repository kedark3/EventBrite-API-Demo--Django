from django import forms
#creating a simple fjango form with one select box with multiple choice enables

class SimpleForm(forms.Form):
    def __init__(self, favorite_event_categories, *args, **kwargs):
        super(SimpleForm, self).__init__(*args, **kwargs)
        self.fields['favorite_event_categories'].choices = favorite_event_categories


    favorite_event_categories = forms.MultipleChoiceField(required=True,
        widget=forms.SelectMultiple(attrs={'size':'20', 'required':'True'}), choices=())
