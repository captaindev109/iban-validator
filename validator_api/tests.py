from django.test import TestCase
from django.urls import reverse

from .models import ValidationHistory

class IBANValidationTestCase(TestCase):

    def test_valid_iban_validation(self):
        # Create a valid IBAN to test
        iban = "ME25505000012345678951"

        # Send a POST request to the validate-iban endpoint with the valid IBAN
        response = self.client.post(
            reverse("validate-iban"),
            {"iban": iban}
        )

        # Assert that the response status code is 200
        self.assertEqual(response.status_code, 200)

        # Assert that the JSON response contains "valid" as true
        self.assertEqual(response.json()["valid"], True)

        # Assert that the validation history is stored in the database
        self.assertEqual(ValidationHistory.objects.count(), 1)
        validation_result = ValidationHistory.objects.first()
        self.assertEqual(validation_result.iban, iban)
        self.assertEqual(validation_result.valid, True)

    def test_invalid_iban_validation(self):
        # Create an invalid IBAN to test
        iban = "ME25505000INVALID"

        # Send a POST request to the validate-iban endpoint with the invalid IBAN
        response = self.client.post(
            reverse("validate-iban"),
            {"iban": iban}
        )

        # Assert that the response status code is 200
        self.assertEqual(response.status_code, 200)

        # Assert that the JSON response contains "valid" as false
        self.assertEqual(response.json()["valid"], False)

        # Assert that the validation history is stored in the database
        self.assertEqual(ValidationHistory.objects.count(), 1)
        validation_result = ValidationHistory.objects.first()
        self.assertEqual(validation_result.iban, iban)
        self.assertEqual(validation_result.valid, False)
    def test_validation_history(self):
        self.client.post(
            reverse("validate-iban"),
            {"iban": "ME25505000012345678951"}
        )
        self.client.post(
            reverse("validate-iban"),
            {"iban": "ME25505000INVALID"}
        )
        # Send a GET request to the validation-history endpoint
        response = self.client.get(reverse("validation-history"))

        # Assert that the response status code is 200
        self.assertEqual(response.status_code, 200)

        # Assert that the JSON response contains the validation history entries
        self.assertEqual(len(response.json()["history"]), 2)
        self.assertEqual(response.json()["history"][0]['valid'], True)
        self.assertEqual(response.json()["history"][1]['valid'], False)