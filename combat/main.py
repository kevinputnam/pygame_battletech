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
            {"name":"melee",
             "damage":2,
             "type":"",
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
             "damage":2,
             "extra_dmg":2,
             "type":"M",
             "heat":0,
             "loc":"l_leg",
             "range":[0,0,-2,None]}
         ],
         "sprite_sheet_path":"../assets/sprites/mech_wasp_2.png",
         "sprite_size":[128,192],
         "directions":{"left":[0],"right":[1]}
     }
}

player_mechs = [mechs.Mech(mech_data['WSP-1A'])]
opposing_mechs = [mechs.Mech(mech_data['WSP-1A'])]

args = {"player_mechs":player_mechs,"opposing_mechs":opposing_mechs}

current_scene = scene.CombatScene(args)

def start():
    ui.initialize_screen("Yo! It's combat!")
    while 1:
        user_input = ui.process_user_input()
        current_scene.run(user_input)
        ui.update_screen()

start()