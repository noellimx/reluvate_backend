from django.db import models

# Create your models here.


class DummyModel(models.Model):

    number = models.IntegerField(null=False)

    def __init__(self):
        print("DummyModel")
