from mashgame.models import Attack, ResultData

class SingleEntity:
    def __init__(self, user, choice):
        self.user = user
        self.choice = choice
        self.active = True

    def deactivate(self):
        self.active = False


class Block4Entity:
    def __init__(self, *args):
        self.entities = list(*args)
        self.active_entities = self.count_active_entities()

    def count_active_entities(self):
        count = 0
        for entity in self.entities:
            count += entity.active.real
        return count

    def activeEntities(self):
        ae = []
        for entity in self.entities:
            if entity.active:
                ae.append(entity)
        return ae

    def activeNEntities(self, expected_active_entities=1):
        return self.activeEntities[:expected_active_entities]

    def deactivate_entity(self, entity):
        entity.deactivate()
        self.active_entities -= 1

    def passBy(self, current_number, start_number=4, end_number=1, incr=-1, expected_active_number=1):
        if not ((start_number<=current_number<=end_number) or (start_number>=current_number>=end_number)):
            raise Exception(f"Current number beyond the boundary:\n\tstart_number: {start_number}\n\tcurrent_number: {current_number}\n\tend_number: {end_number}")
        for entity in self.entities:
            if self.active_entities==expected_active_number:
                return current_number
            if entity.active and current_number == end_number:
                self.deactivate_entity(entity)
                current_number = start_number
            elif entity.active:
                current_number += incr
        return current_number


class MashGame:
    def __init__(self, attack):
        attacker = attack.attacker
        attacker_data = attack.attack_data
        rcvr = attack.reciever
        rcvr_pref = rcvr.preference.mash_data
        self.homes = Block4Entity(
                                [
                                    SingleEntity(rcvr, rcvr_pref.home_1),
                                    SingleEntity(rcvr, rcvr_pref.home_2),
                                    SingleEntity(attacker, attacker_data.home_1),
                                    SingleEntity(attacker, attacker_data.home_2)
                                ]
        )

        self.spouses = Block4Entity(
                                [
                                    SingleEntity(rcvr, rcvr_pref.spouse_1),
                                    SingleEntity(rcvr, rcvr_pref.spouse_2),
                                    SingleEntity(attacker, attacker_data.spouse_1),
                                    SingleEntity(attacker, attacker_data.spouse_2)
                                ]

        )

        self.numchilds = Block4Entity(
                                [
                                    SingleEntity(rcvr, rcvr_pref.numchild_1),
                                    SingleEntity(rcvr, rcvr_pref.numchild_1),
                                    SingleEntity(attacker, attacker_data.numchild_1),
                                    SingleEntity(attacker, attacker_data.numchild_2)
                                ]

        )
        self.luxuries = Block4Entity(
                                [
                                    SingleEntity(rcvr, rcvr_pref.luxury_1),
                                    SingleEntity(rcvr, rcvr_pref.luxury_1),
                                    SingleEntity(attacker, attacker_data.luxury_1),
                                    SingleEntity(attacker, attacker_data.luxury_2)
                                ]

        )


    def start(self, cycle_number):
        print("")
        blocks = [self.homes, self.spouses, self.numchilds, self.luxuries]
        indx = 0
        while(len(blocks)!=0):
            cycle_number = blocks[indx].passBy(cycle_number)
            if blocks[indx].active_entities==1:
                blocks.remove(blocks[indx])
            indx += 1
            if indx >= len(blocks):
                indx = 0
        result = {
                    'home': self.homes.activeEntities()[:1],
                    'spouse': self.spouses.activeEntities()[:1],
                    'numchild': self.numcilds.activeEntities()[:1],
                    'luxury': self.luxuries.activeEntities()[:1]
                 }
        return result



def count_matches(user, result):
    count = 0
    for key in result:
        if result[key].user == user:
            count += 1
    return count


def generateResultDataForAllAttack():
    check = input("tell me your name: ")
    if not check == "mash":
        print("Sorry!")
        return None

    attacks = list(Attack.objects.all())

    # delete attacks which has None on attack_data field
    indx = 0
    while indx < len(attacks):
        if attacks[indx].attack_data==None :
            attacks.remove(attacks[indx])
        else:
            indx += 1

    for attack in attacks:
        if not attack.reasult_data==None:
            continue

        mash_value = attack.attacker.lucky_number+attack.reciever.lucky_number
        mashgame = MashGame(attack)
        result = mashgame.start(mash_value)

        # generate result_data
        attacker_points = count_matches(attack.attacker, result)
        reciever_points = count_matches(attack.reciever, result)

        try:
            result_data = ResultData(
                                        home = result["home"],
                                        spouse = result["spouse"],
                                        numchild = result["numchild"],
                                        luxury = result["luxury"],
                                        available = True,
                                        mash_value = mash_value,
                                        attacker_points = attacker_points,
                                        reciever_points = reciever_points
            )
            result_data.save()
        except Exception as e:
            print(f"Exception happened: for attack: {attack}")
            print("\t", e)
            print("\t", str(e.__class__))
            continue
