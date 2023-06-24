# created 2023-01-12

class Mech:

    def __init__(self,args):
        self.handle = "Flak Bait"
        self.name = "Locust"
        self.designation = "LCT-1V"
        self.type = "mech"
        self.pv = 18
        self.tmm = 3
        self.size = 1 # 1: light; 2: medium; 3: heavy; 4: assualt
        self.damage = [1,1,0] # Short, Medium, Long
        self.melee_bonus = 0
        self.move = 16
        self.jump_jets = False
        self.role = "scout"
        self.skill = 4 # lower is better
        self.ov = 0
        self.armor = 2
        self.structure = 2
        self.orders = {}
        self.disabled = False
        self.mass = 20

        #Choice for current round
        self.jumping = False
        self.attack = "None"
        self.target = -1

        for key in args:
            setattr(self, key, args[key])

        self.hitpoints = self.armor + self.structure

    def long_name(self):
        dis_text = ""
        if self.disabled:
            dis_text = " - DISABLED"
        return self.handle +" (" + self.designation + ")" + dis_text

    def get_pv(self):
        pv_val = self.pv
        if self.disabled:
            pv_val = 0
        return pv_val

shadow_hawk = {"handle":"Blue Beatle",
                    "name":"Shadow Hawk",
                    "designation":"SHD-2H",
                    "pv":30,
                    "size":2,
                    "mass":55,
                    "tmm":2,
                    "move":10,
                    "jump_jets":True,
                    "damage":[2,2,1],
                    "armor":5,
                    "structure":5}

victor = {"handle":"Foe Hammer",
               "name":"Victor",
               "designation":"VTR-9B",
               "pv":36,
               "size":4,
               "mass":80,
               "tmm":1,
               "move":8,
               "jump_jets":True,
               "damage":[4,4,0],
               "armor":6,
               "structure":6}

archer = {"handle":"Hate Storm",
               "name":"Archer",
               "designation":"ARC-2R",
               "pv":39,
               "size":3,
               "mass":70,
               "tmm":1,
               "move":8,
               "damage":[2,3,3],
               "ov":1,
               "armor":7,
               "structure":6}

centurion = {"handle":"Reaver",
                  "name":"Centurion",
                  "designation":"CN9-A",
                  "pv":28,
                  "size":2,
                  "mass":50,
                  "tmm":1,
                  "move":8,
                  "damage":[2,3,1],
                  "armor":5,
                  "structure":4}

hatchetman = {"handle":"Log Splitter",
                  "name":"Hatchetman",
                  "designation":"HCT-3F",
                  "pv":20,
                  "size":2,
                  "mass":45,
                  "tmm":1,
                  "move":8,
                  "jump_jets":True,
                  "damage":[2,2,0],
                  "melee_bonus":1,
                  "armor":3,
                  "structure":4}

vindicator = {"handle":"No Guts? No Glory!",
                  "name":"Vindicator",
                  "designation":"VND-1R",
                  "pv":28,
                  "size":2,
                  "mass":45,
                  "tmm":1,
                  "move":8,
                  "jump_jets":True,
                  "damage":[2,2,2],
                  "armor":5,
                  "structure":4}

warhammer = {"handle":"Canned Heat",
               "name":"Warhammer",
               "designation":"WHM-6D",
               "pv":36,
               "size":3,
               "mass":70,
               "tmm":1,
               "move":8,
               "damage":[3,3,2],
               "ov":0,
               "armor":7,
               "structure":6}

commando = {"handle":"Miss me?",
                    "name":"Commando",
                    "designation":"COM-2D",
                    "pv":15,
                    "size":1,
                    "mass":25,
                    "tmm":2,
                    "move":12,
                    "damage":[2,2,0],
                    "armor":2,
                    "structure":2}