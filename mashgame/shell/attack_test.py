from mashgame.models import *
from .mashgame import *

u1 = User.objects.first()
u2 = User.objects.get(id=4)

a = u1.sentAttackOn(u2)

mg = MashGame(a)
