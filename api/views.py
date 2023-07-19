from django.http import JsonResponse
import shippo

# Set your Shippo API key
shippo.config.api_key = 'shippo_test_07336595ab8adfa17846bc36165cb02a03f161d1'

def get_shipping_rates(request):
    # Define the addresses
    address_from = {
        'name': 'John Doe',
        'street1': '123 Main St',
        'city': 'San Francisco',
        'state': 'CA',
        'zip': '94111',
        'country': 'US'
    }
    address_to = {
        'name': 'Jane Doe',
        'street1': '456 Elm St',
        'city': 'New York',
        'state': 'NY',
        'zip': '10001',
        'country': 'US'
    }

    # Define the parcel
    parcel = {
        'length': '5',
        'width': '5',
        'height': '5',
        'distance_unit': 'in',
        'weight': '10',
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
        print(rates)
        # Prepare the shipping rates response
        shipping_rates = []
        for rate in rates.results:
            shipping_rates.append({
                'service': rate.provider,
                'rate': rate.amount_local
            })

        return JsonResponse({'rates': shipping_rates})

    except Exception as e:
        return JsonResponse({'error': str(e)})
