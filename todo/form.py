from django import forms
from .models import List, ListItem, User

class ListForm(forms.ModelForm):
    class Meta:
        model = List
        fields =['list_name', 'cover_img']



class ListItemForm(forms.ModelForm):
    class Meta:
        model = ListItem
        fields = ['item_text']