from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, get_user_model, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import (
    UserRegistrationForm,
    LoanApplicationForm,
    CreditCardFraudForm,
    GoldPricePredictionForm,
    BitcoinPredictionForm,
)
import pickle
import numpy as np
from django.http import JsonResponse

# Create your views here.


def register_user(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            User = get_user_model()
            username = user.full_name + user.phone_number
            new_user = User.objects.create_user(
                # username=username,
                username=user.email,
                email=user.email,
                password=form.cleaned_data["password1"],
            )
            new_user.save()
            return redirect("login")
    else:
        form = UserRegistrationForm()
    return render(request, "FraudDetection/Auth/register.html", {"form": form})


def login_user(request):
    if request.method == "POST":
        email = request.POST.get("email")  # Assuming email is used for authentication
        password = request.POST.get("password")

        print("Email:", email)  # Debugging statement
        print("Password:", password)  # Debugging statement

        user = authenticate(request, username=email, password=password)
        if user is not None:
            print("User found:", user)  # Debugging statement
            login(request, user)
            # Redirect to a success page or homepage
            return redirect("index")
        else:
            # Authentication failed
            print("No user found")  # Debugging statement
            messages.error(request, "Invalid email or password. Please try again.")
            return redirect("login")  # Redirect to the login page with an error message
    else:
        return render(request, "FraudDetection/Auth/login.html")


@login_required(login_url="login")
def logout_user(request):
    logout(request)
    return redirect("login")


# In views.py


def loan_application_view(request):
    # Load the model
    with open("static/loant.pickle", "rb") as f:
        model = pickle.load(f)

    if request.method == "POST":
        form = LoanApplicationForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)

            # Prepare data for prediction
            data = [
                instance.gender,
                instance.married,
                instance.dependents,
                instance.education,
                instance.self_employed,
                instance.applicant_income,
                instance.coapplicant_income,
                instance.loan_amount,
                instance.loan_amount_term,
                instance.credit_history,
                instance.property_area,
            ]

            # Map data according to model input requirements
            gender_mapping = {"Male": 0, "Female": 1}
            married_mapping = {"Yes": 1, "No": 0}
            education_mapping = {"Graduate": 1, "Not Graduate": 0}
            self_employed_mapping = {"Yes": 1, "No": 0}
            property_area_mapping = {"Urban": 0, "Semiurban": 1, "Rural": 2}

            data[0] = gender_mapping[data[0]]
            data[1] = married_mapping[data[1]]
            data[3] = education_mapping[data[3]]
            data[4] = self_employed_mapping[data[4]]
            data[10] = property_area_mapping[data[10]]

            # Convert all data to numeric types
            try:
                data = list(map(float, data))
            except ValueError as e:
                return JsonResponse({"errors": {"value_error": [str(e)]}})

            # Predict using the model
            prediction = model.predict([data])[0]  # Assuming model expects a 2D array

            # Convert prediction to "True" or "False"
            loan_status = "True" if prediction == 1 else "False"

            # Save instance with the loan status
            instance.loan_status = loan_status
            instance.save()

            # Return JSON response
            return JsonResponse({"loan_status": loan_status})

        # Handle form errors
        return JsonResponse({"errors": form.errors})

    else:
        form = LoanApplicationForm()

    return render(
        request,
        "FraudDetection/LoanApplication/loan_application_form.html",
        {"form": form},
    )


def credit_card_fraud_view(request):
    # Load the model
    with open("static/bcredit_card_fraud_pred.pickle", "rb") as f:
        model = pickle.load(f)

    if request.method == "POST":
        form = CreditCardFraudForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)

            # Prepare data for prediction
            data = [
                instance.age,
                instance.pay_0,
                instance.pay_2,
                instance.pay_3,
                instance.pay_4,
                instance.pay_5,
                instance.pay_6,
                instance.bill_amt1,
                instance.bill_amt2,
                instance.bill_amt3,
                instance.bill_amt4,
                instance.bill_amt5,
                instance.bill_amt6,
            ]

            # Predict using the model
            prediction = model.predict([data])[0]  # Assuming model expects a 2D array

            # Convert prediction to "Fraud" or "Not Fraud"
            fraud_status = "Fraud" if prediction == 1 else "Not Fraud"
            instance.loan_status = fraud_status

            # Detailed criteria evaluation
            criteria = {
                "age": instance.age,
                "pay_0": instance.pay_0,
                "pay_2": instance.pay_2,
                "pay_3": instance.pay_3,
                "pay_4": instance.pay_4,
                "pay_5": instance.pay_5,
                "pay_6": instance.pay_6,
                "bill_amt1": instance.bill_amt1,
                "bill_amt2": instance.bill_amt2,
                "bill_amt3": instance.bill_amt3,
                "bill_amt4": instance.bill_amt4,
                "bill_amt5": instance.bill_amt5,
                "bill_amt6": instance.bill_amt6,
            }

            instance.save()

            return JsonResponse({"status": fraud_status, "criteria": criteria})
        else:
            return JsonResponse({"errors": form.errors}, status=400)

    form = CreditCardFraudForm()
    return render(
        request,
        "FraudDetection/CreditCardFraud/credit_card_fraud_form.html",
        {"form": form},
    )


def service(request):
    #
    return render(request, "FraudDetection/services.html")


def index(request):
    #
    return render(request, "FraudDetection/index.html")


def gold_price_prediction_view(request):
    if request.method == "POST":
        form = GoldPricePredictionForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)

            # Prepare data for prediction
            data = [
                instance.open_price,
                instance.high_price,
                instance.low_price,
                instance.volume,
                instance.change_percent,
                instance.month,
            ]

            try:
                # Load the model
                with open("static/gold-predictionsssss.pickle", "rb") as f:
                    model = pickle.load(f)

                # Ensure that the loaded object is a model
                if not hasattr(model, "predict"):
                    raise ValueError("Loaded object is not a valid model")

                # Predict using the model
                prediction = model.predict([data])[
                    0
                ]  # Assuming model expects a 2D array

                # Save instance with the prediction
                instance.target_price = prediction
                instance.save()

                return JsonResponse({"prediction": prediction})
            except Exception as e:
                return JsonResponse({"errors": str(e)}, status=400)
        else:
            return JsonResponse({"errors": form.errors}, status=400)

    form = GoldPricePredictionForm()
    return render(
        request,
        "FraudDetection/GoldPrediction/gold_price_prediction.html",
        {"form": form},
    )


def bitcoin_price_prediction_view(request):
    if request.method == "POST":
        form = BitcoinPredictionForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)

            # Prepare data for prediction
            data = [
                instance.open_price,
                instance.high_price,
                instance.low_price,
                instance.adj_close,
                instance.volume,
                instance.coin,
                instance.year,
            ]

            try:
                # Load the model
                with open("static/trained_modelss.pkl", "rb") as f:
                    model = pickle.load(f)

                # Ensure that the loaded object is a model
                if not hasattr(model, "predict"):
                    raise ValueError("Loaded object is not a valid model")

                # Predict using the model
                prediction = model.predict([data])[
                    0
                ]  # Assuming model expects a 2D array
                prediction_prob = model.predict_proba([data])[
                    0
                ]  # Get prediction probabilities

                # Interpret the prediction
                result = "Increase" if prediction == 1 else "Decrease"

                # Save instance with the prediction
                instance.prediction = result
                instance.save()

                return JsonResponse(
                    {"prediction": result, "probabilities": prediction_prob.tolist()}
                )
            except Exception as e:
                return JsonResponse({"errors": str(e)}, status=400)
        else:
            return JsonResponse({"errors": form.errors}, status=400)

    form = BitcoinPredictionForm()
    return render(
        request,
        "FraudDetection/BitcoinPrediction/bitcoin_price_prediction.html",
        {"form": form},
    )
