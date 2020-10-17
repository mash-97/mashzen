from django.db import models
from .data import MASHData
from .user import User

class AttackManager(models.Manager):
    def createAAttackWithDefaultMASHData(self, attacker, reciever):
        mash_data = MASHData.objects.getADefaultMASHData()
        attack = Attack(attacker=attacker, reciver=reciever)
        attack.save()
        return attack()


class Attack(models.Model):
    attacker = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_attacks")
    reciever = models.ForeignKey(User, on_delete=models.CASCADE, related_name="recieved_attacks")
    

    def __str__(self):
        return attacker.user_name+" --> "+reciever.user_name
