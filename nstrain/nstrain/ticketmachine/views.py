import json
from django import forms
from django.shortcuts import render
import requests
import pandas as pd
from datetime import datetime

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

way = (
  ('single', 'One way'),
  ('return', 'Return')
)

payment_methods = (
  ('Debit Card', 'Debit Card'),
  ('Credit Card', 'Credit Card'),
  ('Cash', 'Cash')
)

# make a form for ticket
class SelectTicketForm(forms.Form):
  from_station = forms.ChoiceField(choices=stations)
  to_station = forms.ChoiceField(choices=stations)
  travel_class = forms.CharField(label='Travel class', 
  widget=forms.RadioSelect(choices=travel_class))
  way = forms.CharField(label='Way', widget=forms.RadioSelect(choices=way))
  passengers = forms.IntegerField(label="Number of passengers", min_value=1, max_value=10)


# make a form for payment methods
class PaymentForm(forms.Form):
  payment = forms.CharField(label='Payment Method', 
  widget=forms.RadioSelect(choices=payment_methods))


def index(request):
  return render(request, "ticketmachine/index.html", {
      "form": SelectTicketForm({'travel_class': '2', 'way': 
      'single', 'discount': '1', 'passengers': 1})
  })


def planning(request):
  global form_from_station
  global form_to_station
  global form_travel_class
  global form_travelway
  global form_passenger_amount
  if request.method == 'POST':
    form = SelectTicketForm(request.POST)
    if form.is_valid():
      form_from_station = request.POST.get("from_station")
      form_to_station = request.POST.get("to_station")
      form_travel_class = request.POST.get("travel_class")
      form_travelway = request.POST.get("way")
      form_passenger_amount = request.POST.get("passengers")
  if form_from_station != form_to_station:
    return render(request, "ticketmachine/planning.html", {
      "form": PaymentForm({'payment': '1'}),
      "price": get_price(),
      "trips": get_trips()
      })
  else:
    return render(request, "ticketmachine/index.html", {
      "form": SelectTicketForm({
        'travel_class': form_travel_class, 
        'way': form_travelway, 
        'discount': '1', 
        'passengers': form_passenger_amount})
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
          "price": get_price(),
          "trips": get_trips()
          })
  return render(request, "ticketmachine/planning.html", {
    "form": PaymentForm({'payment': '1'}),
    })

def lookup_station(station_uic: str, format: str) -> str:
  stationsDf = pd.read_excel('ticketmachine\stations-2022-01-nl.xlsx')
  if format == "code":
    station = stationsDf.loc[stationsDf['uic'] == int(station_uic)]['code'].values[0]
  elif format == "long_name":
    station = stationsDf.loc[stationsDf['uic'] == int(station_uic)]['name_long'].values[0]
  return station

def ns_send_request( url: str, parameters: dict  ) -> dict:
    headers = {'Ocp-Apim-Subscription-Key': 'f7cb7bf0fdd844658153f525c346baa2'}
    r = requests.get( url, headers=headers, params=parameters )
    data = json.loads(r.content.decode('utf-8'))
    return data
    
def get_trips():
  url = "https://gateway.apiportal.ns.nl/reisinformatie-api/api/v3/trips"
  parameters = {
    'fromStation': lookup_station(form_from_station, "code"),
    'toStation': lookup_station(form_to_station, "code"),
    'dateTime': datetime.now(),
    'travelClass': form_travel_class,
  }
  response = ns_send_request( url, parameters )
  returned_trips = response['trips'][0:5]
  destination = lookup_station(form_to_station, "long_name")

  trips = []
  for trip in returned_trips:
    planned_time = trip['legs'][0]['origin']['plannedDateTime'][:-5]
    planned_time_object = datetime.strptime( planned_time, '%Y-%m-%dT%H:%M:%S').strftime('%H:%M')

    trips.append({"final_destination": destination, "plannedDateTime": planned_time_object,
            "plannedDurationInMinutes": trip['plannedDurationInMinutes'], 
            "transfers": trip['transfers'],
            "crowdForecast": trip['crowdForecast'].title()})
  return trips


def get_price():

  url = "https://gateway.apiportal.ns.nl/reisinformatie-api/api/v2/price"
  parameters = {
    'fromStation': lookup_station(form_from_station, "code"),
    'toStation': lookup_station(form_to_station, "code"),
  }

  response = ns_send_request( url, parameters )

  total_price = response['payload']['totalPriceInCents'] / 100
  total_price = total_price * int(form_passenger_amount)
  if (form_travelway == 'return' ):
    total_price = total_price * 2
  return total_price