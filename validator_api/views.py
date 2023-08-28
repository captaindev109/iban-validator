from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
from .models import ValidationHistory
import json

class ValidateIBANView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request):
        iban = request.POST.get("iban")
        if iban:
            # Add your IBAN validation logic here
            is_valid = self.validate_iban(iban)
            # return JsonResponse({"valid": is_valid})

            # Store the validation result in the database
            ValidationHistory.objects.create(iban=iban, valid=is_valid)

            return JsonResponse({"valid": is_valid})

        return HttpResponseBadRequest(
            json.dumps({"error": "Invalid request. Please check the entered IBAN."}),
            content_type="application/json",
        )

    def validate_iban(self, iban):
        alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        digits = '0123456789'

        # Remove white space and convert to uppercase
        iban = iban.replace(' ', '').upper()

        # Check if length is correct
        if len(iban) < 2 or len(iban) > 34:
            return False

        # Check if first two characters are letters
        if not iban[:2].isalpha():
            return False

        # Check if rest of characters are alphanumeric
        if not iban[2:].isalnum():
            return False

        # Move first four characters to the end
        iban = iban[4:] + iban[:4]

        # Convert letters to numbers
        digits_iban = ''
        for char in iban:
            if char.isalpha():
                digits_iban += str(alphabet.index(char) + 10)
            else:
                digits_iban += char

        # Calculate modulo 97 of the converted IBAN number
        remainder = int(digits_iban) % 97

        return remainder == 1

class ValidationHistoryView(View):
    def get(self, request):
        history = ValidationHistory.objects.all().values(
            "iban", "valid", "timestamp"
        )
        response = {
            "history": list(history)
        }
        return JsonResponse(response)