from django.http import JsonResponse, HttpRequest, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
import shippo
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from hcaptcha.fields import hCaptchaField

@require_POST
def contact_form_submission(request):
    # Validate the form data including the hCaptcha field
    captcha_validator = hCaptchaField()
    form_data = {
        'name': request.POST.get('name'),
        'email': request.POST.get('email'),
        'message': request.POST.get('message'),
        'h-captcha-response': request.POST.get('h-captcha-response'),  # hCaptcha response token
    }

    # Check if the form is valid including the hCaptcha verification
    if captcha_validator.clean(form_data['h-captcha-response']):
        # Process your form data here
        name = form_data['name']
        email = form_data['email']
        message = form_data['message']

        # Perform additional form submission logic if needed

        # Return a success response
        return JsonResponse({'message': 'Form submission successful.'})
    else:
        return JsonResponse({'error': 'Invalid hCaptcha response.'}, status=400)



# Set your Shippo API key
shippo.config.api_key = 'shippo_live_ae12d265315704b900878ff86b7f689508b740c7'
# Global variable to store shipping rates temporarily
shipping_rates_data = []
@csrf_exempt
def shipping_rates_view(request: HttpRequest) -> HttpResponse:
    global shipping_rates_data

    if request.method == 'POST':
        # Extract the JSON data sent from the React frontend
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError as e:
            return JsonResponse({'error': 'Invalid JSON format'}, status=400)

        # Process the data as needed
        address_from = {
            'name': data.get('name_from'),
            'street1': data.get('street1_from'),
            'city': data.get('city_from'),
            'state': data.get('state_from'),
            'zip': data.get('zip_from'),
            'country': data.get('country_from')
        }
        address_to = {
            'name': data.get('name_to'),
            'street1': data.get('street1_to'),
            'city': data.get('city_to'),
            'state': data.get('state_to'),
            'zip': data.get('zip_to'),
            'country': data.get('country_to')
        }
        parcel = {
            'length': data.get('length'),
            'width': data.get('width'),
            'height': data.get('height'),
            'distance_unit': 'in',
            'weight': data.get('weight'),
            'mass_unit': 'lb'
        }

        try:
            # Create the shipment
            shipment = shippo.Shipment.create(
                address_from=address_from,
                address_to=address_to,
                parcels=[parcel],
                asynchronous=False
            )

            # Retrieve the available rates for the shipment
            rates = shippo.Shipment.get_rates(shipment.object_id, asynchronous=False)

            # Prepare the shipping rates response
            shipping_rates = []
            for rate in rates.results:
                shipping_rates.append({
                    'provider': rate.provider,
                    'service': rate.duration_terms,
                    'rate': rate.amount_local+"$"
                })

            # Add some logging to check the rates
            print("Shipping rates:", shipping_rates)

            # Store the shipping rates in the global variable
            shipping_rates_data = shipping_rates

            return JsonResponse({'rates': shipping_rates})

        except Exception as e:
            # Handle any exceptions that occur during shipping rate processing
            return JsonResponse({'error': str(e)}, status=500)

    elif request.method == 'GET':
        # Handle the GET method here to retrieve shipping rates from the global variable
        return JsonResponse({'rates': shipping_rates_data})

    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)


