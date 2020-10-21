from mashgame.models import Attack, ResultData

class SingleEntity:
    def __init__(self, user, choice):
        self.user = user
        self.choice = choice
        self.active = True

    def deactivate(self):
        self.active = False
    def activate(self):
        self.active = True

    def __str__(self):
        a = ""
        if self.active:
            a = " * "
        return f"({self.user.user_name}:{self.choice.value}){a}"


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

    def stringOfActiveEntities(self):
        string = []
        indx = 0
        for entity in self.entities:
            if entity.active:
                string.append(f"({indx+1}. {entity.__str__()})")
                indx += 1
        string = "::".join(string)
        return string

    def deactivate_entity(self, entity):
        entity.deactivate()
        self.active_entities -= 1

    def activateAllEntities(self):
        for entity in self.entities:
            entity.activate()
        self.active_entities = self.count_active_entities()

    def passBy(self, current_number, start_number, end_number=1, expected_active_number=1, tabs=""):
        print("\n")
        print(tabs+f"For block: {self}")
        print(tabs+f"Passed cn: {current_number}, sn: {start_number}, en: {end_number}, ean: {expected_active_number}")
        if not ((start_number<=current_number<=end_number) or (start_number>=current_number>=end_number)):
            raise Exception(tabs+f"Current number beyond the boundary:\n\tstart_number: {start_number}\n\tcurrent_number: {current_number}\n\tend_number: {end_number}")

        incr = -1
        if end_number-start_number >=1:
            incr = 1
        if end_number==start_number:
            raise Exception(tabs+f"Bound Error: end_number-start_number=0")

        for entity in self.entities:
            if self.active_entities==expected_active_number:
                print(tabs+f"\tNumber of active entities: {self.active_entities} == expected_active_number: {expected_active_number}")
                print(tabs+f"\tSo returning with value: {current_number}")
                return current_number
            if entity.active and current_number == end_number:
                print(tabs+f"\tDeactivating: {entity.__str__()}")
                print(tabs+f"\tCurrent Number: {current_number}")
                self.deactivate_entity(entity)
                print(tabs+f"\tAssigning start_number to current_number: {current_number}")
                current_number = start_number
            elif entity.active:
                print(tabs+f"\tFor active entity: {entity.__str__()}")
                current_number += incr
                print(tabs+f"\tIncremented current_number: {current_number}")
        print(tabs+f"returning with current_number: {current_number}")
        return current_number

    def __str__(self):
        string = []
        for entity in self.entities:
            string.append(f"{entity.__str__()}")
        string = "::".join(string)
        return string


class MashGame:
    def __init__(self, attack):
        self.attack = attack
        self.player_2 = attacker = attack.attacker
        attacker_data = attack.attack_data
        self.player_1 = rcvr = attack.reciever
        rcvr_pref = rcvr.preference.mash_data
        self.mash_value = self.player_1.lucky_number+self.player_2.lucky_number
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
        self.blocks = [self.homes, self.spouses, self.numchilds, self.luxuries]
        self.previous_result = None

    def turninInitState(self):
        for block in self.blocks:
            block.activateAllEntities()
        self.previous_result = None

    def start(self, tabs=""):
        print(tabs+"Proceeding on MashGame: ")
        print(tabs+f"\tBetween {self.player_1.user_name} and {self.player_2.user_name}")
        print(tabs+f"\tWith MashValue: {self.mash_value}")
        print(tabs+f"\tHomes: {self.homes}")
        print(tabs+f"\tSpouses: {self.spouses}")
        print(tabs+f"\tNumber of Childs: {self.numchilds}")
        print(tabs+f"\tLuxuries: {self.luxuries}")

        blocks = self.blocks.copy()
        indx = 0
        mash_value = self.mash_value
        while(len(blocks)!=0):
            print(tabs+f"\tindx: {indx}, current_block: #{blocks[indx].__str__()}, mash_value: {mash_value}")
            mash_value = blocks[indx].passBy(mash_value, start_number=self.mash_value, tabs=tabs+"\t")
            print(tabs+f"\tafter passing by active entites: in this block: {blocks[indx].stringOfActiveEntities()}")
            if blocks[indx].active_entities==1:
                blocks.remove(blocks[indx])
            indx += 1
            if indx >= len(blocks):
                indx = 0
        self.previous_result = {
                    'home': self.homes.activeEntities()[0],
                    'spouse': self.spouses.activeEntities()[0],
                    'numchild': self.numchilds.activeEntities()[0],
                    'luxury': self.luxuries.activeEntities()[0]
                 }
        print(tabs+f"\tresult: {self.previous_result}")
        print("\n\n")
        return self.previous_result

    def __str__(self, tabs=""):
        string = tabs+str(self.attack)+"\n"
        string += tabs+"\t{self.homes.__str__()}\n"
        string += tabs+"\t{self.spouses.__str__()}\n"
        string += tabs+"\t{self.numchilds.__str__()}\n"
        string += tabs+"\t{self.luxuries.__str__()}\n"
        if self.previous_result:
            string += tabs+"\tprevious_result: {self.previous_result}"


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

    c = 0
    print(f"Total {len(attacks)} attacks found")
    for attack in attacks:
        print(f"{attack}: ")
        if not attack.result_data==None:
            print(f"\tA result already found!")
            continue

        print(f"\tProceeding on mashgame engine: ", end="")
        mashgame = MashGame(attack)
        result = mashgame.start(tabs="\t")
        print(f"result produced-> {[result[k].__str__() for k in result]}")
        # generate result_data
        attacker_points = count_matches(attack.attacker, result)
        reciever_points = count_matches(attack.reciever, result)

        try:
            result_data = ResultData(
                                        home = result["home"].choice,
                                        spouse = result["spouse"].choice,
                                        numchild = result["numchild"].choice,
                                        luxury = result["luxury"].choice,
                                        available = True,
                                        mash_value = mashgame.mash_value,
                                        attacker_points = attacker_points,
                                        reciever_points = reciever_points
            )
            result_data.save()
            attack.result_data = result_data
            attack.save()
        except Exception as e:
            print(f"\tException happened: for attack: {attack}")
            print("\t", e)
            print("\t", str(e.__class__))
            continue
        print(f"\tResultData saved! id: {result_data.id}")
        print(f"\tPoints:: {attack.reciever}: {result_data.reciever_points}, {attack.attacker}: {result_data.attacker_points}")
        c += 1

    print(f"\n-------__> Total successful result_data produced: {c}")
    print(f"\n-------__> Unsuccessful: {len(attacks)-c}")
