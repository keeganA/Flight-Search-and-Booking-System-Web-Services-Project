from django.db import models

# Create your models here.


##What are the the exact names for the tables??

##What are the exact data types for the fields

class Country(models.Model):
    country_name = models.CharField(max_length=30)
    continent = models.CharField(max_length=30)
    longitude = models.FloatField()
    latitude = models.FloatField()

    def __str__(self):
        return self.country_name
    
class Plane(models.Model):
    max_capacity = models.IntegerField()
    max_flight_distance = models.IntegerField()

    def __str__(self):
        return f"Plane {self.pk}"



class Flight_Instance(models.Model):
    plane_ID = models.ForeignKey(Plane, on_delete=models.CASCADE)
    flight_ticket_cost = models.FloatField()
    departure_country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='departure_flights')
    arrival_country =models.ForeignKey(Country, on_delete=models.CASCADE,related_name='arrival_flights' )
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    num_available_seats = models.IntegerField()
    airline_name = models.CharField(max_length=30)
    def __str__(self):
        return f"Flight_Instance {self.pk}"
    
class Passenger(models.Model):
    booking_ID = models.IntegerField()
    first_name = models.CharField(max_length=30)#check if there is a max
    last_name = models.CharField(max_length=30)#check if there is a max
    date_of_birth = models.DateField()
    nationality_country_ID = models.IntegerField()
    passport_num = models.CharField(max_length=30)
    seat_ID = models.IntegerField()
    def __str__(self):
        return f"Passenger {self.pk}"

##seat_name or seat_id??
class Seat_Instance(models.Model):
    seat_name = models.CharField(max_length=3)
    available = models.BooleanField()
    flight_ID = models.IntegerField()
    def __str__(self):
        return self.seat_name

class Booking_Instance(models.Model):
    booked_at_time = models.DateTimeField()
    lead_passenger_contact_email = models.CharField(max_length= 30)
    lead_passenger_contact_number = models.CharField(max_length= 30)
    total_booking_cost = models.FloatField()
    payment_confirmed = models.BooleanField()
    transcation_ID = models.IntegerField()
    def __str__(self):
        return f"Passenger {self.pk}"





