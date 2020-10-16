
from django.db import models
from .data import MASHData
from .user import User

class PreferenceManager(models.Manager):
    def createAPreferenceWithDefaultMASHData(self, user):
        mash_data = MASHData.objects.getADefaultMASHData()
        preference = Preference(user=user, mash_data=mash_data)
        preference.save()
        return preference

class Preference(models.Model):
    objects = PreferenceManager()
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    mash_data = models.OneToOneField(MASHData, on_delete=models.CASCADE)

    def __str__(self):
        data = [self.mash_data.home_1.value, self.mash_data.spouse_1.value, self.mash_data.numchild_1.value,
                self.mash_data.luxury_1.value]
        return ("|".join(data))
