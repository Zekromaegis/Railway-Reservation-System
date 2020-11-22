from django.contrib import admin
from . import models
# Register your models here.
admin.site.register(models.Profile)
admin.site.register(models.Train)
admin.site.register(models.Trainstatus2)
admin.site.register(models.Ticket2)
admin.site.register(models.Route)
admin.site.register(models.Station)