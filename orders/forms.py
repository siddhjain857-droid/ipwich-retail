from django import forms

class CheckoutForm(forms.Form):
    email = forms.EmailField()
    full_name = forms.CharField(max_length=120)
    address = forms.CharField(max_length=255)
    city = forms.CharField(max_length=120)
    postal_code = forms.CharField(max_length=20)
