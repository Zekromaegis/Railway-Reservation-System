from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def auth_token_generator(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

GENDER_CHOICES = (
    (0,'Male'),
    (1,'Female'),
    (2,'Other'),
)

class Profile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="profile", primary_key=True
    )
    gender = models.IntegerField(choices=GENDER_CHOICES)

    def __str__(self):
        return str(self.user) + "'s profile"

from django.db import models
class Route(models.Model):
    train = models.ForeignKey('Train', models.DO_NOTHING)
    station = models.ForeignKey('Station', models.DO_NOTHING)

    class Meta:
        db_table = 'route'
        unique_together = (('train', 'station'),)

    def __str__(self):
        return str(self.train) + " | " + str(self.station)

class Station(models.Model):
    station_id = models.AutoField(primary_key=True)
    station_name = models.CharField(max_length=30, unique=True)

    class Meta:
        db_table = 'station'
    
    def __str__(self):
        return self.station_name

TICKET_STATUS_CHOICES = (
    ('W','Waiting'),
    ('C','Confirmed'),
)

class Ticket(models.Model):
    ticket_id = models.AutoField(primary_key=True)
    ticket_status = models.CharField(max_length=1,choices=TICKET_STATUS_CHOICES)
    seat_cost = models.IntegerField()
    seat_no = models.IntegerField()
    user = models.ForeignKey(User, models.DO_NOTHING)
    train = models.ForeignKey('Trainstatus', models.DO_NOTHING, related_name='ticket_train')
    departure_date = models.ForeignKey('Trainstatus', models.DO_NOTHING, db_column='departure_date', related_name='ticket_departure_date')

    class Meta:
        db_table = 'ticket'
    
    def __str__(self):
        return f"{self.user} | {self.seat_no} | {self.train} | {self.departure_date}"

TRAIN_TYPES = (
    ('S','Sleeper'),
    ('C','Chair'),
)

class Train(models.Model):
    train_id = models.AutoField(primary_key=True)
    train_type = models.CharField(max_length=1,choices=TRAIN_TYPES)
    train_name = models.CharField(unique=True, max_length=20)
    no_of_seats = models.IntegerField()
    start_station = models.ForeignKey(Station, models.DO_NOTHING, db_column='start_station', related_name='start_station')
    end_station = models.ForeignKey(Station, models.DO_NOTHING, db_column='end_station', related_name='end_station')
    start_time = models.TimeField()
    end_time = models.TimeField()
    seat_cost = models.IntegerField()

    class Meta:
        db_table = 'train'

    def __str__(self):
        return self.train_name + " | " + self.start_station.station_name + " > " + self.end_station.station_name

class Trainstatus(models.Model):
    seats_booked = models.IntegerField()
    train = models.OneToOneField(Train, models.DO_NOTHING, primary_key=True)
    departure_date = models.DateField()
    seat_cost = models.IntegerField()
    total_seats = models.IntegerField()
    waiting = models.IntegerField()

    class Meta:
        db_table = 'trainstatus'
        unique_together = (('train', 'departure_date'),)

class Trainstatus2(models.Model):
    seats_booked = models.IntegerField()
    train = models.ForeignKey(Train, models.CASCADE)
    departure_date = models.DateField()
    seat_cost = models.IntegerField()
    total_seats = models.IntegerField()
    waiting = models.IntegerField()

    class Meta:
        db_table = 'trainstatus2'
        unique_together = (('train', 'departure_date'),)

    def __str__(self):
        return self.train.train_name + " status on " + str(self.departure_date)

class Ticket2(models.Model):
    ticket_id = models.AutoField(primary_key=True)
    ticket_status = models.CharField(max_length=1,choices=TICKET_STATUS_CHOICES)
    seat_cost = models.IntegerField()
    seat_no = models.IntegerField()
    user = models.ForeignKey(User, models.DO_NOTHING)
    trainstatus_id = models.ForeignKey(Trainstatus2, models.DO_NOTHING)

    class Meta:
        db_table = 'ticket2'
    
    def __str__(self):
        return f"{self.user} | {self.seat_no} | {self.train} | {self.departure_date}"