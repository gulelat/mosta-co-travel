from django.contrib import admin

# Register your models here.
from reserve.models import Hotel, Reservation_Company, Comment, Company_Offer, Reserved_Room, Rate, Hotel_Image
admin.site.register(Hotel)
admin.site.register(Reserved_Room)
admin.site.register(Reservation_Company)
admin.site.register(Company_Offer)
admin.site.register(Comment)
admin.site.register(Rate)
admin.site.register(Hotel_Image)