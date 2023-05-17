import json
from django.utils import timezone
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Flight_Instance, Country, Passenger, Seat_Instance, Booking_Instance, Plane
from django.http import JsonResponse ##Can we import this?
import requests##Needed to talk to payments service
from django.core.serializers.json import DjangoJSONEncoder#Needed to correctly format date and time values


# Create your views here.


##just to confirm by "get"ing the fights, we are getting the flight instances and not the planes?
def find_flights(request):
    if request.method == 'GET':
        departure_country = request.GET.get('departure_country', None)
        departure_date = request.GET.get('departure_date', None)
        arrival_country = request.GET.get('arrival_country', None)
        num_passengers = request.GET.get('num_passengers', None)
        max_price = request.GET.get('max_price', None)




        ##get all instances of Flight_Instance first
        queryset = Flight_Instance.objects.all()


        if departure_date:
            queryset = queryset.filter(departure_time__date=departure_date)
        if departure_country:
            queryset = queryset.filter(departure_country__country_name=departure_country)
        if arrival_country:
            queryset = queryset.filter(arrival_country__country_name=arrival_country)
        if max_price:
            queryset = queryset.filter(flight_ticket_cost__lte=max_price)
        if num_passengers:
            queryset = queryset.filter(num_available_seats__gte=num_passengers)
        print("\n\n",queryset.values(),"\n\n")

        #if no Flight_Instance(s) are found then return appropiate response
        if not queryset.exists():
                return HttpResponse("No flights found matching the given criteria.")

        flights_list = []

        ##Note to self
        ## appending '_id' to the field name indicates you are referencing the ID of the related object instead of the actual object itself
        for flight in queryset:
            departure_country_name = Country.objects.get(id=flight.departure_country_id).country_name
            arrival_country_name = Country.objects.get(id=flight.arrival_country_id).country_name

            flight_data = {
                'id':flight.id,
                'flight_ticket_cost': flight.flight_ticket_cost,
                'departure_country': departure_country_name,
                'arrival_country': arrival_country_name,
                'departure_time': flight.departure_time.isoformat(),
                'arrival_time': flight.arrival_time.isoformat(),
                'num_available_seats': flight.num_available_seats,
                'airline_name': flight.airline_name,
                }
            flights_list.append(flight_data)

        return JsonResponse(flights_list, safe=False, status=200)




        







##Do i need to have a function
def find_seats(request):
    if request.method == 'GET':
        flight_id = request.GET.get('flight_id')

        try:
            seats = Seat_Instance.objects.filter(flight_ID=flight_id)
        except Seat_Instance.DoesNotExist:
            return JsonResponse({"message": "No seats found for the given flight ID."}, status=200)

        seats_list = list(seats.values())
        return JsonResponse(seats_list, safe=False, status=200)







@csrf_exempt
def book(request):    
    if request.method == 'POST'and request.content_type == 'application/json':
        request_data = json.loads(request.body)

    
        flight_id = request_data.get('flight_id')
        lead_passenger_contact_email = request_data.get('lead_passenger_contact_email')
        lead_passenger_contact_number = request_data.get('lead_passenger_contact_number')


        all_instances_of_flight_id = Flight_Instance.objects.filter(id=flight_id).value("flight_ticket_cost")
        total_booking_cost = all_instances_of_flight_id["flight_ticket_cost"] * len(all_instances_of_flight_id)
        
        ##First make a booking instance as the id of this booking will be needed for the passengers

        booking_instance = Booking_Instance.objects.create(
            booked_at_time=timezone.now(),
            lead_passenger_contact_email=lead_passenger_contact_email,
            lead_passenger_contact_number= lead_passenger_contact_number,
            total_booking_cost=total_booking_cost,
            payment_confirmed=False,
            transcation_ID=None)

        booking_instance_id = booking_instance.id

        passengers = request_data.get('passengers', [])

                      
        ##Go through the passengers list and add to db
        for i in range(len(passengers)):
            current_passenger = passengers[i]
            first_name = current_passenger.get('first_name')
            last_name = current_passenger.get('last_name')
            date_of_birth = current_passenger.get("date_of_birth") 
            nationality_country = current_passenger.get("nationality_country") 
            passport_number = current_passenger.get("passport_number")
            seat_name = current_passenger.get("seat_name")


            Passenger.objects.create(
                booking_ID=booking_instance_id,
                first_name= first_name,
                last_name= last_name,
                date_of_birth=date_of_birth,
                nationality_country=nationality_country,
                passport_number=passport_number,
                seat_name=seat_name
                )
            

        ##Now get payment details
        payment_details = request_data.get('payment_details', {})
        cardholder_name = payment_details.get('cardholder_name')
        card_number = payment_details.get('card_number')
        cvc = payment_details.get('cvc')
        expiry_date = payment_details.get('expiry_date')
        sortcode = payment_details.get('sortcode')






        ##Now needs confirm payment with payment__api
        url = '/pay'
        data={
            'sender_cardholder_name':cardholder_name,
            'sender_card_number_hash':card_number,
            'sender_cvc_hash':cvc,
            'sender_expiry_date':expiry_date,
            'recipient_cardholder_name':payment_details['keeganAirline'],##Get details from payment database
            'recipient_sortcode':payment_details['232323'],#Get details from payment database
            'recipient_account_number':payment_details['365555721'],#Get details from payment database
            'payment_amount':total_booking_cost
        }
        
        payment_response = requests.post(url, json=data)
            

        
        if payment_response.status_code == 200:
            booking_instance.payment_confirmed=True
            booking_instance.transacation_ID = payment_response.json().get('transcation_ID')
            booking_instance.save()
        else:
            return HttpResponse("Payment failed", status=payment_response.status_code)
        
        booking_instance.transcation_ID=response["transcation_ID"]


        ##Now need to create response in the required format

        response = {
            "id": booking_instance.id,
            "booked_at_time": booking_instance.booked_at_time.isoformat(),
            "lead_passenger_contact_email": booking_instance.lead_passenger_contact_email,
            "lead_passenger_contact_number": booking_instance.lead_passenger_contact_number,
            "total_booking_cost": booking_instance.total_booking_cost,
            "payment_confirmed": booking_instance.payment_confirmed,
            "transaction_id": booking_instance.transaction_ID
        }

        return JsonResponse(response, status=200)



        
def delete(request):
    
    if request.method == 'DELETE':
        request_data = json.loads(request.body)

        booking_id = request_data.get('booking_id')
        account_number = request_data.get('account_number')
        lead_passenger_contact_email = request_data.get('lead_passenger_contact_email')
        sortcode = request_data.get('sortcode')

        booking_instance_to_be_deleted = Booking_Instance.objects.get(id=booking_id)
        total_booking_cost = booking_instance_to_be_deleted.total_booking_cost

        
        url = '/pay'
        data={
            'sender_cardholder_name':"keeganAirline",
            'sender_card_number_hash':'8d5a6c72c000deb233690427d006b9e4b394146d7c84cc7cbf1ed1d93e3552d336136da5d31e82dc4868d62069a9537c',
            'sender_cvc_hash': '9a0a82f0c0cf31470d7affede3406cc9aa8410671520b727044eda15b4c25532a9b5cd8aaf9cec4919d76255b6bfb00f',
            'sender_expiry_date':'02/2025',
            ##'recipient_cardholder_name': I might need it i might not
            'recipient_sortcode':sortcode,
            'recipient_account_number':account_number,
            'payment_amount':total_booking_cost
        }
        ##refund
        payment_response = requests.post(url, json=data)

        if payment_response.status_code == 200:
            return JsonResponse(status=200)


def update(request):

 if request.method == 'PUT':
        request_data = json.loads(request.body)

        booking_id = request_data.get('booking_id')
        first_name = request_data.get('first_name')
        last_name = request_data.get('last_name')
        seat_name = request_data.get('seat_name')


        passenger = Passenger.objects.get(booking_id=booking_id, first_name=first_name, last_name=last_name)
        passenger.seat_name = seat_name
        passenger.save()

        return JsonResponse(status=200)













def get_booking(request):
    if request.method == 'GET':
        booking_id = request.GET.get('id')


        try:
            booking_instance = Booking_Instance.objects.get(id=booking_id)
            response = {
                "id": booking_instance.id,
                "booked_at_time": booking_instance.booked_at_time.strftime('%Y-%m-%dT%H:%M:%S'),
                "total_booking_cost": booking_instance.total_booking_cost,
                "transaction_id": booking_instance.transcation_ID,
                "payment_confirmed": booking_instance.payment_confirmed,
                "flight_id": booking_instance.flight.id
            }
            return JsonResponse(response, status=200, encoder=DjangoJSONEncoder)
        except Booking_Instance.DoesNotExist:
            return HttpResponse("Booking not found.", status=404)    

    






 












    

        
        
        

        
