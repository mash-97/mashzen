from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.exceptions import ValidationError
from django.utils import timezone
import hashlib

import mashgame

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
                """ create a default preference """
                from .preference import Preference
                Preference.objects.assignByDefault(user=user)
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

    def login(self, user_name, password):
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
        except Exception as exception:
            print("\tException Happened: ", exception)
            print("\t\texception class: ", exception.__class__)
        return None

    def getUsersAgainst(self, user):
        users_list = list(User.objects.all())
        users_list.remove(user)
        for tuser in users_list:
            if tuser.recievedAttackFrom(user):
                tuser.attack_status = "attacked"
            else:
                tuser.attack_status = "attack"
        return users_list

    def getUserAgainst(self, user, reciever_name):
        users_list = self.getUsersAgainst(user)
        for u in users_list:
            if u.user_name==reciever_name:
                return u
        return None

    def getSortedUsersBasedOnResult(self):
        users_list = list(User.objects.all())

        for u in users_list:
            # add attribute as total_points, tp_recieved_attacks, tp_sent_attacks
            u.total_points = 0
            u.tp_recieved_attacks = 0
            u.tp_sent_attacks = 0
            # produce points from recieved_attacks
            attacks = u.recievedAttacks()
            for recieved_attack in attacks:
                try:
                    if recieved_attack.result_data:
                        u.tp_recieved_attacks += recieved_attack.result_data.reciever_points
                except mashgame.models.attack.Attack.result_data.RelatedObjectDoesNotExist:
                    continue

            # produce points from sent_attacks
            attacks = u.sentAttacks()
            for sent_attack in attacks:
                try:
                    if sent_attack.result_data:
                        u.tp_sent_attacks += sent_attack.result_data.attacker_points
                except mashgame.models.attack.Attack.result_data.RelatedObjectDoesNotExist:
                    continue
            u.total_points = u.tp_sent_attacks + u.tp_recieved_attacks
        # sort based on total_points attribute
        users_list.sort(key = lambda x: x.total_points, reverse=True)
        return users_list


class User(models.Model):
    objects = UserManager()
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"
    SECRET = "secret"
    GENDERS = [(MALE, "Male"), (FEMALE, "Female"), (OTHER, "Other"), (SECRET, "Secret")]

    user_name = models.CharField(max_length=20, unique=True)
    password = models.CharField(max_length=10)
    gender = models.CharField(max_length=7, choices=GENDERS, default=SECRET)
    visit_count = models.IntegerField(default=0)
    lucky_number = models.IntegerField(default=3, validators=[validate_1_to_10])

    def sentAttackOn(self, user):
        attack = None
        try:
            attack = self.sent_attacks.filter(reciever__id=user.id)
            if attack.exists():
                attack = attack.first()
            else:
                attack = None
        except Exception as exception:
            message = f"""Exception Happened on recievedAttacks() call:\n\tException Type: {exception.__class__}\n\tMessage: {exception}"""
            self.log(message)
        return attack

    def sentAttacks(self):
        attacks = None
        try:
            attacks = list(self.sent_attacks.all())
        except Exception as exception:
            message = f"""Exception Happened on recievedAttacks() call:\n\tException Type: {exception.__class__}\n\tMessage: {exception}"""
            self.log(message)
        return attacks


    def recievedAttackFrom(self, user):
        attack = None
        try:
            attack = self.recieved_attacks.filter(attacker__id=user.id)
            if attack.exists():
                attack = attack.first()
            else:
                attack = None
        except Exception as exception:
             message = f"""Exception Happened on recievedAttacks() call:\n\tException Type: {exception.__class__}\n\tMessage: {exception}"""
             self.log(message)
        return attack


    def recievedAttacks(self):
        attacks = None
        try:
            attacks = list(self.recieved_attacks.all())
        except Exception as exception:
            message = f"""Exception Happened on recievedAttacks() call:\n\tException Type: {exception.__class__}\n\tMessage: {exception}"""
            self.log(message)
        return attacks


    def log(self, message):
        log = UserLog(message=message, user=self)
        log.save()

    def authorize(self, password):
        self.visit_count += 1
        if self.password==password:
            # Create a AuthorizedHash
            # first produce a hash value
            hash_value = hashlib.sha1((self.user_name+str(timezone.now())).encode()).hexdigest()
            authorized_hash = AuthorizedHash(value=hash_value, user=self)
            authorized_hash.save()
        else:
            return False
        self.save()
        self.log(f"Successful authorization attempt.\n\tHash Value: {authorized_hash.value}")
        return authorized_hash.value

    def deauthorizeHash(self, hash_value):
        authorized_hash = self.hashes.filter(value=hash_value)
        if authorized_hash.exists():
            authorized_hash.first().delete()
            self.log(f"Successful deauthorization of hash value: {hash_value}")

    def hashValues(self):
        return [hash.value for hash in self.hashes.all()]

    def __str__(self):
        return self.user_name




class AuthorizedHash(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="hashes")
    value = models.CharField(max_length=50, unique=True)



class UserLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="logs")
    creation_time = models.DateTimeField(auto_now=True)
    message = models.CharField(max_length=1024)

    def __str__(self):
        return self.message
