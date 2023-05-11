from django.db import models

# Create your models here.


##What are the the exact names for the tables??

##What are the exact data types for the fields


class Flight_Instance(models.Model):
    plane_ID = models.IntegerField()
    flight_ticket_cost = models.FloatField()
    departure_location_ID = models.IntegerField()
    arrival_location_ID = models.IntegerField()
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    num_available_seats = models.IntegerField()

class Passenger(models.Model):
    booking_ID = models.IntegerField()
    first_name = models.CharField(max_length=30)#check if there is a max
    last_name = models.CharField(max_length=30)#check if there is a max
    date_of_birth = models.DateField()
    nationality_country_ID = models.IntegerField()
    passport_num = models.CharField(max_length=30)
    seat_ID = models.IntegerField()

##seat_name or seat_id??
class Seat_Instance(models.Model):
    seat_name = models.CharField(max_length=30)
    available = models.BooleanField()
    flight_ID = models.IntegerField()

class Booking_Instance(models.Model):
    booked_at_time = models.DateTimeField()
    lead_passenger_contact_email = models.CharField(max_length= 30)
    lead_passenger_contact_number = models.CharField(max_length= 30)
    total_booking_cost = models.FloatField()
    payment_confirmed = models.BooleanField()
    transcation_ID = models.IntegerField()



class Plane(models.Model):
    max_capacity = models.IntegerField()
    max_flight_distance = models.IntegerField()



class Country(models.Model):
    country_name = models.CharField(max_length=30)
    continent = models.CharField(max_length=30)
    longitude = models.FloatField()
    latitude = models.FloatField()

