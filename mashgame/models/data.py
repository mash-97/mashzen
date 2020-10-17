from django.db import models

class Home(models.Model):
    value =  models.CharField(max_length=100, default="Home")
    def __str__(self):
        return self.value

class Spouse(models.Model):
    value =  models.CharField(max_length=100, default="Spouse Name")
    def __str__(self):
        return self.value

class NumChild(models.Model):
    value =  models.CharField(max_length=100, default="Number of Childs")
    def __str__(self):
        return self.value

class Luxury(models.Model):
    value =  models.CharField(max_length=100, default="Luxury")
    def __str__(self):
        return self.value

class MASHDataManager(models.Manager):
    DEFAULT_HOME_1 = Home.objects.get(id=1)
    DEFAULT_HOME_2 = Home.objects.get(id=10)
    DEFAULT_SPOUSE_1 = Spouse.objects.get(id=1)
    DEFAULT_SPOUSE_2 = Spouse.objects.get(id=5)
    DEFAULT_NUMCHILD_1 = NumChild.objects.get(id=1)
    DEFAULT_NUMCHILD_2 = NumChild.objects.get(id=4)
    DEFAULT_LUXURY_1 = Luxury.objects.get(id=1)
    DEFAULT_LUXURY_2 = Luxury.objects.get(id=3)

    def getADefaultMASHData(self):
        mash_data = MASHData(home_1 = MASHDataManager.DEFAULT_HOME_1,
                             home_2 = MASHDataManager.DEFAULT_HOME_2,
                             spouse_1 = MASHDataManager.DEFAULT_SPOUSE_1,
                             spouse_2 = MASHDataManager.DEFAULT_SPOUSE_2,
                             numchild_1 = MASHDataManager.DEFAULT_NUMCHILD_1,
                             numchild_2 = MASHDataManager.DEFAULT_NUMCHILD_2,
                             luxury_1 = MASHDataManager.DEFAULT_LUXURY_1,
                             luxury_2 = MASHDataManager.DEFAULT_LUXURY_2)
        mash_data.save()
        return mash_data


class MASHData(models.Model):
    objects = MASHDataManager()
    home_1 = models.ForeignKey(Home, on_delete=models.SET_NULL, related_name="+", null=True)
    home_2 = models.ForeignKey(Home, on_delete=models.SET_NULL, related_name="+", null=True)

    spouse_1 = models.ForeignKey(Spouse, on_delete=models.SET_NULL, related_name="+", null=True)
    spouse_2 = models.ForeignKey(Spouse, on_delete=models.SET_NULL, related_name="+", null=True)

    numchild_1 = models.ForeignKey(NumChild, on_delete=models.SET_NULL, related_name="+", null=True)
    numchild_2 = models.ForeignKey(NumChild, on_delete=models.SET_NULL, related_name="+", null=True)

    luxury_1 = models.ForeignKey(Luxury, on_delete=models.SET_NULL, related_name="+", null=True)
    luxury_2 = models.ForeignKey(Luxury, on_delete=models.SET_NULL, related_name="+", null=True)

    def __str__(self):
        return (self.home_1.value+":"+self.spouse_1.value+":"+self.numchild_1.value+":"+self.luxury_1.value)


class ResultMASHData(models.Model):
    home = models.ForeignKey(Home, on_delete=models.SET_NULL, null=True, related_name="+")
    spouse = models.ForeignKey(Spouse, on_delete=models.SET_NULL, null=True, related_name="+")
    numchild = models.ForeignKey(NumChild, on_delete=models.SET_NULL, null=True, related_name="+")
    luxury = models.ForeignKey(Luxury, on_delete=models.SET_NULL, null=True, related_name="+")
    mash_value = models.IntegerField(default=0)

    
