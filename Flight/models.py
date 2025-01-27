from django.db import models


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
    FLIGHT_TYPES = [
        ('domestic', 'Domestic'),
        ('international', 'International'),
    ]

    TRIP_TYPES = [
        ('direct', 'Direct'),
        ('indirect', 'Indirect'),
    ]

    CABIN_TYPES = [
        ('economy', 'Economy'),
        ('business', 'Business Class'),
        ('first', 'First Class'),
    ]

    flight_number = models.CharField(max_length=50, unique=True)  # شماره پرواز
    flight_type = models.CharField(max_length=15, choices=FLIGHT_TYPES)  # نوع پرواز (داخلی/خارجی)
    trip_type = models.CharField(max_length=15, choices=TRIP_TYPES)  # نوع سفر (مستقیم/غیرمستقیم)
    departure_airport = models.ForeignKey('Airport', on_delete=models.CASCADE, related_name='departures')  # فرودگاه مبدا
    arrival_airport = models.ForeignKey('Airport', on_delete=models.CASCADE, related_name='arrivals')  # فرودگاه مقصد
    departure_datetime = models.DateTimeField()  # تاریخ و ساعت تیکاف
    arrival_datetime = models.DateTimeField()  # تاریخ و ساعت لندینگ
    airline = models.ForeignKey('Airline', on_delete=models.CASCADE)  # ایرلاین
    aircraft = models.ForeignKey('Aircraft', on_delete=models.CASCADE)  # هواپیما
    cabin_type = models.CharField(max_length=20, choices=CABIN_TYPES)  # نوع کابین
    base_price = models.BigIntegerField()  # قیمت پایه
    tax = models.DecimalField(max_digits=5, decimal_places=2, default=0)  # مالیات به صورت درصد
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # تخفیف به صورت درصد
    baggage_limit_kg = models.DecimalField(max_digits=10, decimal_places=2)  # میزان بار مجاز (کیلوگرم)
    flight_rules = models.TextField()  # قوانین و مقررات پرواز

    def __str__(self):
        return self.flight_number

    @property
    def capacity(self):
        """Return Capacity From Aircraft"""
        return self.aircraft.aircraft_capacity

    @property
    def final_price(self):
        """
        Calculate Final Price with tax & discount
        """
        # Calculate discounted price
        discounted_price = self.base_price * (1 - (self.discount / 100))
        # Calculate final price with tax
        final_price = discounted_price * (1 + (self.tax / 100))
        return round(final_price)