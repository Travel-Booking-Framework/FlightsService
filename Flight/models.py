from django.db import models
from enum import Enum


class FlightType(Enum):
    DOMESTIC = "Domestic"
    INTERNATIONAL = "International"


class TripType(Enum):
    DIRECT = "Direct"
    INDIRECT = "Indirect"


class CabinType(Enum):
    ECONOMY = "Economy"
    BUSINESS = "Business Class"
    FIRST = "First Class"


class Airline(models.Model):
    airline_name = models.CharField(max_length=255)
    airline_code = models.CharField(max_length=10, unique=True)
    airline_rules = models.TextField()
    airline_logo = models.ImageField(upload_to='airline_logos/', blank=True, null=True)  # فیلد لوگو

    def __str__(self):
        return f"{self.airline_name} - {self.airline_code}"


class Airport(models.Model):
    airport_name = models.CharField(max_length=255)
    airport_code = models.CharField(max_length=10, unique=True)
    airport_city = models.CharField(max_length=255)
    airport_country = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.airport_name} - {self.airport_code}"


class Aircraft(models.Model):
    aircraft_model = models.CharField(max_length=255, unique=True)  # مدل هواپیما
    aircraft_capacity = models.IntegerField()  # ظرفیت کلی هواپیما
    aircraft_manufacturer = models.CharField(max_length=255)  # سازنده هواپیما

    def __str__(self):
        return f"{self.aircraft_manufacturer} - {self.aircraft_model}"


class Flight(models.Model):
    cabin_type = models.CharField(
        max_length=20,
        choices=[(tag.name, tag.value) for tag in CabinType]
    )
    trip_type = models.CharField(
        max_length=15,
        choices=[(tag.name, tag.value) for tag in TripType]
    )
    flight_type = models.CharField(
        max_length=15,
        choices=[(tag.name, tag.value) for tag in FlightType]
    )
    flight_number = models.CharField(max_length=50, unique=True)  # شماره پرواز
    departure_airport = models.ForeignKey('Airport', on_delete=models.CASCADE, related_name='departures')  # فرودگاه مبدا
    arrival_airport = models.ForeignKey('Airport', on_delete=models.CASCADE, related_name='arrivals')  # فرودگاه مقصد
    departure_datetime = models.DateTimeField()  # تاریخ و ساعت تیکاف
    arrival_datetime = models.DateTimeField()  # تاریخ و ساعت لندینگ
    airline = models.ForeignKey('Airline', on_delete=models.CASCADE)  # ایرلاین
    aircraft = models.ForeignKey('Aircraft', on_delete=models.CASCADE)  # هواپیما
    base_price = models.BigIntegerField()  # قیمت پایه
    tax = models.DecimalField(max_digits=5, decimal_places=2, default=0)  # مالیات به صورت درصد
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # تخفیف به صورت درصد
    baggage_limit_kg = models.DecimalField(max_digits=10, decimal_places=2)  # میزان بار مجاز (کیلوگرم)
    flight_rules = models.TextField()  # قوانین و مقررات پرواز
    final_price = models.BigIntegerField()

    def __str__(self):
        return self.flight_number

    @property
    def capacity(self):
        """Return Capacity From Aircraft"""
        return self.aircraft.aircraft_capacity

    @property
    def final_price_calculated(self):
        """
        Calculate Final Price with tax & discount.
        """
        discounted_price = self.base_price * (1 - (self.discount / 100))
        final_price = discounted_price * (1 + (self.tax / 100))
        return round(final_price)

    def save(self, *args, **kwargs):
        """
        Automatically calculate final price before saving the instance.
        """
        self.final_price = self.final_price_calculated  # محاسبه و ذخیره `final_price` در دیتابیس
        super().save(*args, **kwargs)