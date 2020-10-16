
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.exceptions import ValidationError

from django.utils import timezone
import hashlib

# validator for integer between 1 to 10
def validate_1_to_10(value):
    if not 1<=value<=9:
        raise ValidationError(f"{value} isn't between 1 and 9")


class UserManager(models.Manager):
    def signup(self, user_name, password):
        print("Trying to Create A New User: ", user_name)
        try:
            user = User.objects.create(user_name=user_name, password=password)
            if user:
                print("\tUser created: setting preference: ")
                # create a default preference
                from .preference import Preference
                Preference.objects.createAPreferenceWithDefaultMASHData(user)
                print("\tPreference saved!")
                print("\n")
            else:
                print("\tFailed:\n")
                return False
        except Exception as e:
            print("\n\tException happened!\n", e.__class__)
            print(e)
            return False
        user.save()
        return self.get_authorized_user(user_name, password)

    def get_authorized_user(self, user_name, password):
        print("Trying authorization for: ")
        print("\tuser_name: ", user_name)
        print("\tpassword: ", password)

        try:
            user = User.objects.get(user_name=user_name)
            print("\tUser Found!")
            authorized_hash = user.authorize(password)
            if authorized_hash:
                return {"user": user, "user_hash": authorized_hash}
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

    def setAPreference(self):
        pass

    def authorize(self, password):
        if self.password==password:
            self.authorized = True
            # Create a AuthorizedHash
            # first produce a hash value
            hash_value = hashlib.sha1((self.user_name+str(timezone.now())).encode()).hexdigest()
            authorized_hash = AuthorizedHash(value=hash_value, user=self)
            authorized_hash.save()
        else:
            self.authorized = False
            self.save()
            return False

        self.save()
        return authorized_hash.value

    def deauthorizeHash(self, hash_value):
        authorized_hash = self.hashes.filter(value=hash_value)
        if authorized_hash.exists():
            authorized_hash.first().delete()


    def __str__(self):
        return self.user_name




class AuthorizedHash(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="hashes")
    value = models.CharField(max_length=50, unique=True)



class UserLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    creation_time = models.DateTimeField(auto_now=True)
    message = models.CharField(max_length=1024)
