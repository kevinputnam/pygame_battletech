import ui
import scene
import actor
import mechs

mech_data = {"WSP-1A":{
         "type":"WSP-1A",
         "name":"WASP",
         "movement":3,
         "jump_jets":True,
         "heat_sinks":2,
         "armor":{
            "head":[1,1],
            "torso":[2,2],
            "r_arm":[1,1],
            "l_arm":[1,1],
            "r_leg":[2,1],
            "l_leg":[2,1]
         },
         "equipment":[
            {"name":"punch",
             "damage":1,
             "type":"melee",
             "heat":0,
             "loc":"none",
             "range":[0,None,None,None]},
             {"name":"kick",
             "damage":2,
             "type":"melee",
             "heat":0,
             "loc":"none",
             "range":[0,None,None,None]},
            {"name":"medium laser",
             "damage":2,
             "type":"E",
             "heat":1,
             "loc":"r_arm",
             "range":[0,0,-2,None]},
             {"name":"SRM 2",
             "damage":1,
             "max_dmg":2,
             "type":"M",
             "heat":0,
             "loc":"l_leg",
             "range":[0,0,-2,None]}
         ],
         "sprite_sheet_path":"../assets/sprites/mech_wasp.png",
         "sprite_size":[128,192],
         "directions":{"right":[0],"left":[1]}
     },"LCT-1V":{
         "type":"LCT-1V",
         "name":"LOCUST",
         "movement":4,
         "jump_jets":False,
         "heat_sinks":2,
         "armor":{
            "head":[3,1],
            "torso":[3,2],
            "r_arm":[1,1],
            "l_arm":[1,1],
            "r_leg":[3,1],
            "l_leg":[3,1]
         },
         "equipment":[
            {"name":"kick",
             "damage":2,
             "type":"Melee",
             "heat":0,
             "loc":"none",
             "range":[0,None,None,None]},
            {"name":"medium laser",
             "damage":2,
             "type":"E",
             "heat":1,
             "loc":"torso",
             "range":[0,0,-2,None]},
             {"name":"machine guns",
             "damage":2,
             "type":"B",
             "heat":0,
             "loc":"arms",
             "range":[0,0,None,None]}
         ],
         "sprite_sheet_path":"../assets/sprites/mech_locust.png",
         "sprite_size":[128,192],
         "directions":{"right":[0],"left":[1]}
     }
}


player_mechs = [mechs.Mech(mech_data['WSP-1A']),mechs.Mech(mech_data['LCT-1V'])]
player_mechs[0].gunnery = 2
opposing_mechs = [mechs.Mech(mech_data['LCT-1V']),mechs.Mech(mech_data['WSP-1A'])]

args = {"player_mechs":player_mechs,"opposing_mechs":opposing_mechs}

current_scene = scene.CombatScene(args)

def start():
    ui.initialize_screen("Yo! It's combat!")
    while 1:
        user_input = ui.process_user_input()
        current_scene.run(user_input)
        ui.update_screen()

start()