from django import forms


ANNOUNCE_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 101)]


class CartAddAnnounceForm(forms.Form):
    quantity = forms.TypedChoiceField(choices=ANNOUNCE_QUANTITY_CHOICES, coerce=int)
    update = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)

    quantity.widget.attrs.update({'class': 'btn btn-secondary'})
