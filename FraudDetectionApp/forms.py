from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import (
    User,
    LoanApplication,
    CreditCardFraud,
    GoldPricePrediction,
    BitcoinPrediction,
)


class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = [
            "full_name",
            "email",
            "phone_number",
            "sex",
            "country",
            "age",
            "password1",  # Use 'password1' for the password field
        ]
        widgets = {
            "password1": forms.PasswordInput(),  # Render the password input type
        }


class LoanApplicationForm(forms.ModelForm):
    class Meta:
        model = LoanApplication
        fields = [
            "gender",
            "married",
            "dependents",
            "education",
            "self_employed",
            "applicant_income",
            "coapplicant_income",
            "loan_amount",
            "loan_amount_term",
            "credit_history",
            "property_area",
        ]


class CreditCardFraudForm(forms.ModelForm):
    class Meta:
        model = CreditCardFraud
        fields = [
            "age",
            "pay_0",
            "pay_2",
            "pay_3",
            "pay_4",
            "pay_5",
            "pay_6",
            "bill_amt1",
            "bill_amt2",
            "bill_amt3",
            "bill_amt4",
            "bill_amt5",
            "bill_amt6",
        ]


class GoldPricePredictionForm(forms.ModelForm):
    class Meta:
        model = GoldPricePrediction
        fields = [
            "open_price",
            "high_price",
            "low_price",
            "volume",
            "change_percent",
            "month",
        ]


class BitcoinPredictionForm(forms.ModelForm):
    class Meta:
        model = BitcoinPrediction
        fields = [
            "open_price",
            "high_price",
            "low_price",
            "adj_close",
            "volume",
            "coin",
            "year",
        ]

        widgets = {
            "open_price": forms.NumberInput(
                attrs={"class": "form-control", "placeholder": "Open Price"}
            ),
            "high_price": forms.NumberInput(
                attrs={"class": "form-control", "placeholder": "High Price"}
            ),
            "low_price": forms.NumberInput(
                attrs={"class": "form-control", "placeholder": "Low Price"}
            ),
            "adj_close": forms.NumberInput(
                attrs={"class": "form-control", "placeholder": "Adjusted Close Price"}
            ),
            "volume": forms.NumberInput(
                attrs={"class": "form-control", "placeholder": "Volume"}
            ),
            "coin": forms.NumberInput(
                attrs={"class": "form-control", "placeholder": "Coin"}
            ),
            "year": forms.NumberInput(
                attrs={"class": "form-control", "placeholder": "Year"}
            ),
        }
