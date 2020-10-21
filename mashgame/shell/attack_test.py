from mashgame.models import *
from .mashgame import *

u1 = User.objects.first()
u2 = User.objects.get(id=4)

a = u1.sentAttackOn(u2)

mg = MashGame(a)

def showAttackResultS():
    for attack in Attack.objects.all():
        if attack.result_data:
            print(attack)
            print("result: ")
            print(f"\tHome: {attack.result_data.home}")
            print(f"\tSpouse: {attack.result_data.spouse}")
            print(f"\tNumChild: {attack.result_data.numchild}")
            print(f"\tLuxury: {attack.result_data.luxury}")
            print(f"\tattacker points: {attack.result_data.attacker_points}")
            print(f"\treciever points: {attack.result_data.reciever_points}")
            print("\n\n")
