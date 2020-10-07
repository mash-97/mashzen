from django.db import models

# Create your models here.
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.exceptions import ValidationError

# validator for integer between 1 to 10
def validate_1_to_10(value):
    if not 1<=value<=9:
        raise ValidationError(f"{value} isn't between 1 and 9")


class User(models.Model):
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"
    SECRET = "secret"
    GENDERS = [(MALE, "Male"), (FEMALE, "Female"), (OTHER, "Other"), (SECRET, "secret")]

    user_name = models.CharField(max_length=20)
    pass_code = models.CharField(max_length=10)
    gender = models.CharField(max_length=7, choices=GENDERS, default=SECRET)

    def __str__(self):
        return self.user_name


class Preference(models.Model):
    user = models.OneToOne(User, one_delete=models.CASCADE)
    home_1 = models.CharField(max_length=100, default="Home")
    home_2 = models.CharField(max_length=100, default=None)
    spouse_1 = models.CharField(max_length=100, default="Nina")
    spouse_2 = models.CharField(max_length=100, default=None)
    numchild_1 = models.CharField(max_length=100, default="2")
    numchild_2 = models.CharField(max_length=100, default=None)
    luxury_1 = models.CharField(max_length=100, default="A Cup Of Coffee")
    luxury_2 = models.CharField(max_length=100, default=None)
    lucky_number = models.IntegerField(default=3, validators=[validate_1_to_10])

    def __str__(self):
        return (self.home_1+"|"+self.spouse_1+"|"+self.numchild_1+"|"+self.luxury_1+"|"+str(self.lucky_number))
