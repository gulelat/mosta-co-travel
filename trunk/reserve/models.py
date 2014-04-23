from django.db import models
# Create your models here.
from django.db.models.fields import CharField


class Hotel(models.Model):
    hotel_name = models.CharField(max_length=150)
    hotel_add = models.CharField(max_length=250)
    single_price = models.FloatField()
    num_of_singles = models.IntegerField()
    double_price = models.FloatField()
    num_of_doubles = models.IntegerField()
    triple_price = models.FloatField()
    num_of_triples = models.IntegerField()
    suite_price = models.FloatField()
    num_of_suites = models.IntegerField()
    hotel_url = models.CharField(max_length=250)
    def __unicode__(self):
        return "%s" % (self.hotel_name)

class Reservation_Company(models.Model):
    company_name = models.CharField(max_length=100)
    company_contact = models.CharField(max_length=150)

class Reserved_Room(models.Model):
    hotel_f_id = models.ForeignKey(Hotel)
    room_type = models.CharField(max_length=50)
    check_in_date = models.DateField('start date of reservation ')
    check_out_date = models.DateField('end date of reservation ')
    num_of_rooms = models.IntegerField()

class Company_Offer(models.Model):
    company_name = models.CharField(max_length=100)
    company_f_id = models.ForeignKey(Reservation_Company)
    hotel_f_id = models.ForeignKey(Hotel)
    discount = models.FloatField()
    start = models.DateField('time of start of offer')
    end = models.DateField('time of end of offer')

class Comment(models.Model):
    comment = models.CharField(max_length=500)
    hotel_f_id = models.ForeignKey(Hotel)

class Rate(models.Model):
    RATING = (
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
    )
    rate = models.CharField(max_length=5,choices=RATING, default='3')
    hotel_f_id = models.ForeignKey(Hotel)

class Hotel_Image(models.Model):
    image = models.ImageField(upload_to='images/')
    hotel_f_id = models.ForeignKey(Hotel)