from django.db import models

# Create your models here.
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.exceptions import ValidationError

# validator for integer between 1 to 10
def validate_1_to_10(value):
    if not 1<=value<=9:
        raise ValidationError(f"{value} isn't between 1 and 9")


class MASHData(models.Model):
    home_1 = models.CharField(max_length=100, default="Home")
    home_2 = models.CharField(max_length=100, default=None)
    spouse_1 = models.CharField(max_length=100, default="Nina")
    spouse_2 = models.CharField(max_length=100, default=None)
    numchild_1 = models.CharField(max_length=100, default="2")
    numchild_2 = models.CharField(max_length=100, default=None)
    luxury_1 = models.CharField(max_length=100, default="A Cup Of Coffee")
    luxury_2 = models.CharField(max_length=100, default=None)

    def __str__(self):
        return ()


class UserManager(models.Manager):

    def check_if_username_exist(self, user_name):
        try:
            user = User.objects.get(user_name=user_name)
            return True
        except User.DoesNotExist:
            return False
        return False

    def get_authorized_user(self, user_name, password):
        print("Trying authorization for: ")
        print("\tuser_name: ", user_name)
        print("\tpassword: ", password)

        try:
            user = User.objects.get(user_name=user_name)
            print("\tUser Found!")
            if user.authorize(password):
                return user
            else:
                print("\tFailed on authorization!")
                return None
        except User.DoesNotExist:
            print("\tException Happened: ", User.DoesNotExist)
            return None


class User(models.Model):
    objects = UserManager()
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"
    SECRET = "secret"
    GENDERS = [(MALE, "Male"), (FEMALE, "Female"), (OTHER, "Other"), (SECRET, "secret")]

    user_name = models.CharField(max_length=20, unique=True)
    password = models.CharField(max_length=10)
    gender = models.CharField(max_length=7, choices=GENDERS, default=SECRET)
    authorized = models.BooleanField(default=False)

    visit_count = models.IntegerField(default=0)
    lucky_number = models.IntegerField(default=3, validators=[validate_1_to_10])

    def log(self, message):
        log = UserLog(message=message, user=self)
        log.save()

    def authorize(self, password):
        if self.password==password:
            self.authorized = True
        else:
            self.authorized = False
        self.save()

        return self.authorized

    def __str__(self):
        data = [self.home_1, self.spouse_1, self.numchild_1,
                self.luxury_1, str(self.lucky_number)]
        return "|".join(data)





class UserLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    creation_time = models.DateTimeField(auto_now=True)
    message = models.CharField(max_length=1024)



class Attack(models.Model):
    attacker = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_attacks")
    reciever = models.ForeignKey(User, on_delete=models.CASCADE, related_name="recieved_attacks")
    mash_data = models.OneToOneField(MASHData, on_delete=models.CASCADE)

    def __str__(self):
        return attacker.user_name+" --> "+reciever.user_name


class Preference(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    mash_data = models.OneToOneField(MASHData, on_delete=models.CASCADE)

    def __str__(self):
        data = [self.mash_data.home_1, self.mash_data.spouse_1, self.mash_data.numchild_1,
                self.mash_data.luxury_1, str(self.mash_data.lucky_number)]
        return ("|".join(data))
