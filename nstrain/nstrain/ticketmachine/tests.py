from django.test import TestCase, Client
import unittest
import requests
import pandas as pd
import json

stationsDf = pd.read_excel('ticketmachine\stations-2022-01-nl.xlsx')

class TicketTestCase(TestCase):

    # ADD YOUR TEST FUNCTIONS HERE

    def test_index(self):
        c = Client()
        # Set up client to make requests

        # Send get request to index page and store response
        response = c.get("/ticketmachine/")

        # Make sure status code is 200
        self.assertEqual(response.status_code, 200)


class PriceTestCase(TestCase):
  fromStation= "8400470" # Nijmegen
  endStation= "8400621" # Utrecht
  travelWay= "return" # Single or return trip
  amountPassengers= "5"
  expectedResult= 163
  def getprice(self):
      url = "https://gateway.apiportal.ns.nl/reisinformatie-api/api/v2/price"
      headers = {'Ocp-Apim-Subscription-Key': 'f7cb7bf0fdd844658153f525c346baa2'}
      beginStation = stationsDf.loc[stationsDf['uic'] == int(self.fromStation)]['code'].values[0]
      toStation = stationsDf.loc[stationsDf['uic'] == int(self.endStation)]['code'].values[0]
      parameters = {
        'fromStation': beginStation,
        'toStation': toStation,
      }
      r = requests.get( url, headers=headers, params=parameters )
      data = json.loads(r.content.decode('utf-8'))

      total_price = data['payload']['totalPriceInCents'] / 100
      total_price = total_price * int(self.amountPassengers)
      if (self.travelWay == 'return' ):
        total_price = total_price * 2
      return total_price
  def TestPrices(self):
    assert self.getprice() == self.expectedResult

test_PriceTestCase = PriceTestCase()
test_PriceTestCase.TestPrices()

class PriceTestCase(TestCase):
  fromStation= "8400470" # Nijmegen
  endStation= "8400621" # Utrecht
  travelWay= "return" # Single or return trip
  amountPassengers= "5"
  expectedResult= 163
  def getprice(self):
      url = "https://gateway.apiportal.ns.nl/reisinformatie-api/api/v2/price"
      headers = {'Ocp-Apim-Subscription-Key': 'f7cb7bf0fdd844658153f525c346baa2'}
      beginStation = stationsDf.loc[stationsDf['uic'] == int(self.fromStation)]['code'].values[0]
      toStation = stationsDf.loc[stationsDf['uic'] == int(self.endStation)]['code'].values[0]
      parameters = {
        'fromStation': beginStation,
        'toStation': toStation,
      }
      r = requests.get( url, headers=headers, params=parameters )
      data = json.loads(r.content.decode('utf-8'))

      total_price = data['payload']['totalPriceInCents'] / 100
      total_price = total_price * int(self.amountPassengers)
      if (self.travelWay == 'return' ):
        total_price = total_price * 2
      return total_price
  def TestPrices(self):
    assert self.getprice() == self.expectedResult