from django.db import models
from .data import MASHData, ResultData
from .user import User

class AttackManager(models.Manager):
    def assignByDefault(self, attacker, reciever):
        attack_data = MASHData.objects.getDefault()
        result_data = ResultData.objects.getDefault()
        attack = Attack(attacker=attacker, reciever=reciever, attack_data=attack_data)
        attack.save()
        return attack


class Attack(models.Model):
    objects = AttackManager()
    attacker = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_attacks")
    reciever = models.ForeignKey(User, on_delete=models.CASCADE, related_name="recieved_attacks")
    attack_data = models.OneToOneField(MASHData, on_delete=models.CASCADE, related_name="attack_data", null=True, default=None)
    result_data = models.OneToOneField(ResultData, on_delete=models.CASCADE, related_name="result_data", null=True, default=None)

    def __str__(self):
        return self.attacker.user_name+" --> "+self.reciever.user_name
