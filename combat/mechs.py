import actor

class Mech():

    def __init__(self,attr_dict):

        self.name = 'a mech'
        self.type = 'me-6h'

        self.weight_class = 'light'
        self.tonnage = 20

        self.piloting = 1
        self.gunnery = 1
        self.tactics = 1

        self.equipment = [
            {"name":"melee",
             "damage":1,
             "type":"",
             "heat":0,
             "loc":"none",
             "range":[0,None,None,None]}
            ]
        self.armor = {
            "head":[1,1],
            "torso":[1,1],
            "r_arm":[1,1],
            "l_arm":[1,1],
            "r_leg":[1,1],
            "l_leg":[1,1]
        }

        self.heat_level = 0
        self.heat_sinks = 0

        self.movement = 1
        self.jump_jets = False

        self.location = [0,0]

        for key in attr_dict:
            setattr(self,key,attr_dict[key])

        if 'sprite_sheet_path' in attr_dict:
            self.sprite = actor.Actor(self.location[0],self.location[1],self.sprite_sheet_path,self.sprite_size,self.directions)
