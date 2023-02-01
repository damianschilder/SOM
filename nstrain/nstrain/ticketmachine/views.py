from django.shortcuts import render
from django import forms
import requests
import json
import pandas as pd
from datetime import datetime

stationsDf = pd.read_excel('ticketmachine\stations-2022-01-nl.xlsx')

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

payment_methods = (('Debit Card', 'Debit Card'),
                   ('Credit Card', 'Credit Card'),
                   ('Cash', 'Cash')
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
    global fromStation
    global endStation
    global travelClass
    global travelWay
    global amountPassengers
    if request.method == 'POST':
      form = SelectTicketForm(request.POST)
      if form.is_valid():
        fromStation = request.POST.get("from_station")
        endStation = request.POST.get("to_station")
        travelClass = request.POST.get("travel_class")
        travelWay = request.POST.get("way")
        amountPassengers = request.POST.get("passengers")
    return render(request, "ticketmachine/planning.html", {
        "form": PaymentForm({'payment': '1'}),
        "price": getprice(),
        "trips": gettrips()
    })


def payment(request):
    if request.method == "POST":
        form = PaymentForm(request.POST)
        if form.is_valid():
            payment_method = request.POST.get('payment')
            if payment_method == 'Debit Card':
                text_payment = 'Connecting to your debit card'
                return render(request, "ticketmachine/payment.html", {
                    "payment_method": text_payment,
            })
            if payment_method == 'Credit Card':
                text_payment = 'Connecting to your credit card'
                return render(request, "ticketmachine/payment.html", {
                    "payment_method": text_payment,
            })
            if payment_method == 'Cash':
                text_payment = 'Please insert cash'
                return render(request, "ticketmachine/payment.html", {
                    "payment_method": text_payment,
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
    beginStation = stationsDf.loc[stationsDf['uic'] == int(fromStation)]['code'].values[0]
    toStation = stationsDf.loc[stationsDf['uic'] == int(endStation)]['code'].values[0]
    now = datetime.now()

    url = "https://gateway.apiportal.ns.nl/reisinformatie-api/api/v3/trips"
    headers = {'Ocp-Apim-Subscription-Key': 'f7cb7bf0fdd844658153f525c346baa2'}
    parameters = {
      'fromStation': beginStation,
      'toStation': toStation,
      'dateTime': now,
      'travelClass': travelClass,
    }
    r = requests.get( url, headers=headers, params=parameters )
    data = json.loads(r.content.decode('utf-8'))

    trips = [{"final_destination": "Amsterdam Centraal", "plannedDateTime": "2023-01-18 10:48",
              "plannedDurationInMinutes": "38", "transfers": "2",
              "crowdForecast": "normal"}]
    trips = []
    returnedTrips = data['trips'][0:5]
    destination = stationsDf.loc[stationsDf['uic'] == int(endStation)]['name_long'].values[0]
    for trip in returnedTrips:
      plannedTime = trip['legs'][0]['origin']['plannedDateTime'][:-5]
      plannedTimeObject = datetime.strptime( plannedTime, '%Y-%m-%dT%H:%M:%S').strftime('%H:%M')

      trips.append({"final_destination": destination, "plannedDateTime": plannedTimeObject,
              "plannedDurationInMinutes": trip['plannedDurationInMinutes'], "transfers": trip['transfers'],
              "crowdForecast": trip['crowdForecast'].title()})
    return trips


def getprice():
    url = "https://gateway.apiportal.ns.nl/reisinformatie-api/api/v2/price"
    headers = {'Ocp-Apim-Subscription-Key': 'f7cb7bf0fdd844658153f525c346baa2'}

    beginStation = stationsDf.loc[stationsDf['uic'] == int(fromStation)]['code'].values[0]
    toStation = stationsDf.loc[stationsDf['uic'] == int(endStation)]['code'].values[0]
    parameters = {
      'fromStation': beginStation,
      'toStation': toStation,
    }
    r = requests.get( url, headers=headers, params=parameters )
    data = json.loads(r.content.decode('utf-8'))

    total_price = data['payload']['totalPriceInCents'] / 100
    total_price = total_price * int(amountPassengers)
    if (travelWay == 'return' ):
      total_price = total_price * 2
    return total_price
