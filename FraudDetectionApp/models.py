from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser):
    full_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, blank=True)
    sex = models.CharField(
        max_length=10,
        choices=[("Male", "Male"), ("Female", "Female"), ("Other", "Other")],
    )
    country = models.CharField(max_length=100, blank=True)
    age = models.IntegerField(blank=True, null=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["full_name"]

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class LoanApplication(models.Model):
    GENDER_CHOICES = [
        ("Male", "Male"),
        ("Female", "Female"),
    ]

    MARRIED_CHOICES = [
        ("Yes", "Yes"),
        ("No", "No"),
    ]

    EDUCATION_CHOICES = [
        ("Graduate", "Graduate"),
        ("Not Graduate", "Not Graduate"),
    ]

    SELF_EMPLOYED_CHOICES = [
        ("Yes", "Yes"),
        ("No", "No"),
    ]

    PROPERTY_AREA_CHOICES = [
        ("Urban", "Urban"),
        ("Semiurban", "Semiurban"),
        ("Rural", "Rural"),
    ]

    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    married = models.CharField(max_length=3, choices=MARRIED_CHOICES)
    dependents = models.CharField(
        max_length=10
    )  # Assuming this is a string for values like '0', '1', '2', '3+'
    education = models.CharField(max_length=15, choices=EDUCATION_CHOICES)
    self_employed = models.CharField(max_length=3, choices=SELF_EMPLOYED_CHOICES)
    applicant_income = models.IntegerField()
    coapplicant_income = models.IntegerField()
    loan_amount = models.IntegerField()
    loan_amount_term = models.IntegerField()
    credit_history = models.FloatField()
    property_area = models.CharField(max_length=20, choices=PROPERTY_AREA_CHOICES)

    def __str__(self):
        return f"{self.id} - {self.loan_status}"


class CreditCardFraud(models.Model):
    age = models.IntegerField()
    pay_0 = models.IntegerField()
    pay_2 = models.IntegerField()
    pay_3 = models.IntegerField()
    pay_4 = models.IntegerField()
    pay_5 = models.IntegerField()
    pay_6 = models.IntegerField()
    bill_amt1 = models.FloatField()
    bill_amt2 = models.FloatField()
    bill_amt3 = models.FloatField()
    bill_amt4 = models.FloatField()
    bill_amt5 = models.FloatField()
    bill_amt6 = models.FloatField()
    loan_status = models.CharField(
        max_length=10, blank=True, null=True
    )  # For storing the prediction result

    def __str__(self):
        return f"Fraud Prediction {self.id} - {self.loan_status}"


class GoldPricePrediction(models.Model):
    open_price = models.FloatField()
    high_price = models.FloatField()
    low_price = models.FloatField()
    volume = models.FloatField()
    change_percent = models.FloatField()
    month = models.IntegerField()
    target_price = models.FloatField()  # The price we want to predict

    def __str__(self):
        return f"Gold Price Prediction {self.id} - Target: {self.target_price}"


class BitcoinPrediction(models.Model):
    open_price = models.FloatField()
    high_price = models.FloatField()
    low_price = models.FloatField()
    adj_close = models.FloatField()
    volume = models.FloatField()
    coin = models.FloatField()
    year = models.IntegerField()
    prediction = models.CharField(max_length=10, blank=True, null=True)  # This field will store the prediction result

    def __str__(self):
        return f"Prediction {self.id} - {self.prediction}"