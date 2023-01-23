from django.test import TestCase, Client


class TicketTestCase(TestCase):

    # ADD YOUR TEST FUNCTIONS HERE

    def test_index(self):
        c = Client()
        # Set up client to make requests

        # Send get request to index page and store response
        response = c.get("/ticketmachine/")

        # Make sure status code is 200
        self.assertEqual(response.status_code, 200)
