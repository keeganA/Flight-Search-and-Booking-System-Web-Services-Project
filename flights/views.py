from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Flight_Instance, Country, Passenger, Seat_Instance, Booking_Instance, Plane
from django.http import JsonResponse ##Can we import this?

# Create your views here.


##just to confirm by "get"ing the fights, we are getting the flight instances and not the planes?
def find_flights(request):
    if request.method == 'GET':
        departure_country = request.GET.get('departure_country', None)
        departure_date = request.GET.get('departure_date', None)
        arrival_country = request.GET.get('arrival_country', None)
        num_passengers = request.GET.get('num_passengers', None)
        max_price = request.GET.get('max_price', None)
        ##Is max price required 

        ## 1)First check to see what id the country is
        ## 2)once you have the id to the country, use that value to filter out Flight_Instances

        ##Getting the ID of the departure country
        try:
            departure_country_id = Country.objects.get(country_name=departure_country).id
        except Country.DoesNotExist:
            return HttpResponse("No country with this name exists.", status=404)
        except Country.MultipleObjectsReturned:
            return HttpResponse("There are multiple Country instances with this name?")

        ##Getting the ID of the arrival country
        try:
            arrival_country_id = Country.objects.get(country_name=arrival_country).id
        except Country.DoesNotExist:
            return HttpResponse("No country with this name exists.", status=404)
        except Country.MultipleObjectsReturned:
            return HttpResponse("There are multiple Country instances with this name?")


        flights = Flight_Instance.objects.filter(arrival_location_ID=arrival_country_id, departure_location_ID=departure_country_id, departure_time__date=departure_date, num_available_seats__gte=num_passengers, flight_ticket_cost__lte=max_price)


        ##Turn flights QuerySet into a list of dictionaries 
        flights_list = list(flights.values('id', 'departure_location_ID', 'arrival_location_ID', 'departure_time', 'arrival_time', 'num_available_seats', 'flight_ticket_cost'))

        # Replace country IDs with country names since that what the output needs
        for flight in flights_list:
            departure_country = Country.objects.get(id=flight['departure_location_ID']).country_name
            arrival_country = Country.objects.get(id=flight['arrival_location_ID']).country_name
            flight['departure_country'] = departure_country
            flight['arrival_country'] = arrival_country
            del flight['departure_location_ID']
            del flight['arrival_location_ID']

        # Return as JsonResponse
        
        return JsonResponse(flights_list, safe=False)









def find_seats(request):
    return HttpResponse('not yet implemented')
@csrf_exempt
def book(request):
    return HttpResponse('not yet implemented')

def delete(request):
    return HttpResponse('not yet implemented')

def get_booking(request):
    return HttpResponse('not yet implemented')

def update(request):
    return HttpResponse('not yet implemented')

def Check_booking(request):
    return HttpResponse('not yet implemented')


 
