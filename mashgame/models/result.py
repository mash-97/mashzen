from django.db import models
from .attack import Attack
from .data import *

class ResultDataManager(models.Manager):
    def getDefault(self, attack=None):
        result = ResultData(attack=attack)
        result.save()
        return result


class ResultData(models.Model):
    objects = ResultDataManager()
    home = models.ForeignKey(Home, on_delete=models.SET_NULL, null=True, related_name="+")
    spouse = models.ForeignKey(Spouse, on_delete=models.SET_NULL, null=True, related_name="+")
    numchild = models.ForeignKey(NumChild, on_delete=models.SET_NULL, null=True, related_name="+")
    luxury = models.ForeignKey(Luxury, on_delete=models.SET_NULL, null=True, related_name="+")
    mash_value = models.IntegerField(default=0)
    available = models.BooleanField(default=False)
    attacker_points = models.IntegerField(default=0)
    reciever_points = models.IntegerField(default=0)
    attack = models.OneToOneField(Attack, on_delete=models.CASCADE, related_name="result_data", null=True, default=None)
    
    def __str__(self):
        return f"avalable: {self.available}"
