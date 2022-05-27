from django import forms


class SearchForms(forms.Form):
    search = forms.CharField(max_length=10)
    search.widget.attrs.update(size='15')


class NewEntryForm(forms.Form):
    title = forms.CharField(max_length=50)
    text = forms.CharField(widget=forms.Textarea(), label="")


class EditForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea(), label="")
