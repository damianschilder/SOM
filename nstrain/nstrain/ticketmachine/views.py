from django.shortcuts import render
from django import forms

# (STATION UIcCODE, STATION NAME)
stations = (
    ("8400621", "Utrecht Centraal"),
    ("8400282", "Den Haag Centraal"),
    ("8400530", "Rotterdam Centraal"),
    ("8400058", "Amsterdam Centraal"),
    ("8400206", "Eindhoven Centraal"),
    ("8400263", "Groningen"),
    ("8400597", "Tilburg"),
    ("8400055", "Amersfoort Centraal"),
    ("8400071", "Arnhem Centraal"),
    ("8400390", "Leiden Centraal"),
    ("8400470", "Nijmegen"),
    ("8400131", "Breda"),
    ("8400170", "Delft"),
    ("8400285", "Haarlem")
)

travel_class = (
    ('1', 'First class'),
    ('2', 'Second class'),
)

way = (('single', 'One way'),
       ('return', 'Return')
       )

payment_methods = (('1', 'Debit Card'),
                   ('2', 'Credit Card'),
                   ('3', 'Cash')
                   )


# make a form for ticket
class SelectTicketForm(forms.Form):
    from_station = forms.ChoiceField(choices=stations)
    to_station = forms.ChoiceField(choices=stations)
    travel_class = forms.CharField(label='Travel class', widget=forms.RadioSelect(choices=travel_class))
    way = forms.CharField(label='Way', widget=forms.RadioSelect(choices=way))
    passengers = forms.IntegerField(label="Number of passengers", min_value=1, max_value=10)


# make a form for payment methods
class PaymentForm(forms.Form):
    payment = forms.CharField(label='Payment Method', widget=forms.RadioSelect(choices=payment_methods))


def index(request):
    return render(request, "ticketmachine/index.html", {
        "form": SelectTicketForm({'travel_class': '2', 'way': 'single', 'discount': '1', 'passengers': 1})
    })


def planning(request):
    return render(request, "ticketmachine/planning.html", {
        "form": PaymentForm({'payment': '1'}),
        "price": getprice(),
        "trips": gettrips()
    })


def payment(request):
    if request.method == "POST":
        form = PaymentForm(request.POST)
        if form.is_valid():
            payment_method = "1"
            return render(request, "ticketmachine/payment.html", {
                "payment_method": payment_method,
            })
        else:
            return render(request, "ticketmachine/planning.html", {
                "form": form,
                "price": getprice(),
                "trips": gettrips()
            })
    return render(request, "ticketmachine/planning.html", {
        "form": PaymentForm({'payment': '1'}),
    })


def gettrips():
    url = "https://gateway.apiportal.ns.nl/reisinformatie-api/api/v3/trips"
    headers = {'Ocp-Apim-Subscription-Key': 'PUT_YOUR_AUTHORIZATION_KEY_HERE'}

    # SEND A PROPER REQUEST TO URL AND POPULATE "trips" WITH REQUIRED FIELDS IN THE RESPONSE OF API
    trips = [{"final_destination": "Amsterdam Centraal", "plannedDateTime": "2023-01-18 10:48",
              "plannedDurationInMinutes": "38", "transfers": "2",
              "crowdForecast": "normal"}]
    return trips


def getprice():
    url = "https://gateway.apiportal.ns.nl/reisinformatie-api/api/v2/price"
    headers = {'Ocp-Apim-Subscription-Key': 'PUT_YOUR_AUTHORIZATION_KEY_HERE'}

    # SEND A PROPER REQUEST TO URL AND POPULATE "total_price" WITH "totalPriceInCents" FIELD IN THE RESPONSE
    total_price = 12.32
    return total_price
