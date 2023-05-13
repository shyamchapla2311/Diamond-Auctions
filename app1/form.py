from django import forms
from .models import BuyerRegister,SellerRegister

class BuyerRegisterForm(forms.ModelForm):
    class Meta:
        model=BuyerRegister
        fields='__all__'

class SellerRegisterForm(forms.ModelForm):
    class Meta:
        model=SellerRegister
        fields='__all__'