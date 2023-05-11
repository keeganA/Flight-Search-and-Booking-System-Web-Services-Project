from django.contrib import admin

from .models import Flight_Instance, Passenger, Seat_Instance, Booking_Instance, Plane, Country
# Register your models here.

admin.site.register(Flight_Instance)
admin.site.register(Passenger)
admin.site.register(Seat_Instance)
admin.site.register(Booking_Instance)
admin.site.register(Plane)
admin.site.register(Country)




