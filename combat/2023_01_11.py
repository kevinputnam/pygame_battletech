# 01/03 - started the project
# 01/04 - got boundary checking and added some other cool stuff
# 01/05 - encapsulates user input collection and moves team one iteration loop into get orders
# 01/06 - forgot to create a new file in the morning, so overwrote some of 01/05 ... bunch of changes
#       - alternating round resolution working
#       - moved attacks into mech definition and automatically adds DFA if has jump jets
#       - movement is based on whole team
#       - jump jets increase move rate of unit by factor of 1.2
# 01/09 - Adds Out of Range and Disengage to range list to track when someone has fled
#       - Adds game loop to call resolve round until weapons range reaches Disengage
#       - Moved attacks out of mech definition
#       - Added collecting combat orders from player
#       - Jump jet bonues to average movement is only accrued if unit is jumping
#       - Melee, Charge, and DFA are only available at PB range. DFA is only available if jumping
#       - Adds rudimentary damage dealing
#       - Game ends when all of opposing team are disabled
# 01/10 - Minor changes made on my Mac
#       - Readability and interface improvements
#       - Creates long_name method for mech class to combine designation and handle (adds DISABLED if true)
#       - Disabled units are removed from movement and attack consideration
#       - Enemy can now attack and move
#       - TODO - add more units to test with
# 01/11 - Adds Victor, Archer, Shadow Hawk, and Centurions

import random

class Mech:

    def __init__(self,args):
        self.handle = "Flak Bait"
        self.name = "Locust"
        self.designation = "LCT-1V"
        self.type = "mech"
        self.tmm = 3
        self.size = 1 # 1: light; 2: medium; 3: heavy; 4: assualt
        self.damage = [1,1,0] # Short, Medium, Long
        self.move = 16
        self.jump_jets = False
        self.role = "scout"
        self.skill = 4
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

move_rate_jj_adjustment = 1.2
relative_range = 42
ranges = ["PB","Short","Medium","Long","Out of Range","Disengage"]
range_max_values = [1,6,24,42,60,61]
move_orders = ["Withdraw","Close","Hold"]
attacks = ["Fire","Melee","Charge","DFA","None"]


def roll2d(modifiers=[]):
    ms = 0
    for m in modifiers:
        ms += m
    return random.randint(1,6)+random.randint(1,6) + ms

def resolve_initiative(friendlies,enemies):
    player_init = 0
    opposing_init = 0
    while player_init == opposing_init:
        player_init = roll2d()
        opposing_init = roll2d()
    if player_init > opposing_init:
        print("***** Player wins initiative. *****")
        return True
    print("***** Enemy wins initiatve. *****")
    return False

def get_user_input_from_list(prompt,choices):
    print(prompt)
    counter = 1
    for choice in choices:
        print("  " + str(counter) + ". " + choice)
        counter += 1
    selection_num = -1
    while not (selection_num >= 1 and selection_num <= len(choices)):
        selection_text = input("Enter a number from 1-" + str(len(choices)) + ": ")
        if selection_text.isdigit():
            selection_num = int(selection_text)
    return choices[selection_num - 1]

def get_user_choice_from_list(prompt,choices):
    print(prompt)
    counter = 1
    for choice in choices:
        print("  " + str(counter) + ". " + choice)
        counter += 1
    selection_num = -1
    while not (selection_num >= 1 and selection_num <= len(choices)):
        selection_text = input("Enter a number from 1-" + str(len(choices)) + ": ")
        if selection_text.isdigit():
            selection_num = int(selection_text)
    return selection_num - 1

def get_user_input_yes_no(prompt):
    user_input = 'r'
    while not user_input in ["y","n"]:
        user_input = input(prompt + " (y/n) ")
    if user_input == 'y':
        return True
    return False

def get_avg_move_rate(units):
    avg_movement_rate = 0
    unit_counter = 0
    for unit in units:
        if not unit.disabled:
            unit_move = unit.move
            if unit.jump_jets:
                if unit.jumping:
                    unit_move = unit.move * move_rate_jj_adjustment
            avg_movement_rate += unit_move
            unit_counter += 1
    if unit_counter != 0:
        avg_movement_rate = avg_movement_rate/unit_counter
    else:
        avg_movement_rate = 0
    return avg_movement_rate

def get_range_band(current_range):
    counter = 0
    for r in range_max_values:
        if current_range <= r:
            break
        counter += 1
    if counter == len(range_max_values):
        counter -= 1
    return counter

def get_enemy_movement_order(units,opposing):
    tonnage = 0
    for unit in units:
        if not unit.disabled:
            tonnage += unit.mass
    opposing_tonnage = 0
    for unit in opposing:
        if not unit.disabled:
            opposing_tonnage += unit.mass
    if tonnage >= opposing_tonnage:
        return("Close")
    return("Withdraw")

def get_movement_order(units):
    # choose movement for the entire team initiative loser goes first
    for unit in units:
        if not unit.disabled:
            if unit.jump_jets:
                unit.jumping = get_user_input_yes_no("Will " + unit.long_name() + " use jump jets (required for DFA)?")
    return get_user_input_from_list("Select move option for your team: ",move_orders)

def resolve_movement(friendly_order,enemy_order,friendlies,enemies):
    global relative_range

    friendly_speed = get_avg_move_rate(friendlies)
    enemy_speed = get_avg_move_rate(enemies)
    if friendly_order == "Close":
        relative_range -= friendly_speed
    if enemy_order == "Close":
        relative_range -= enemy_speed
    if friendly_order == "Withdraw":
        relative_range += friendly_speed
    if enemy_order == "Withdraw":
        relative_range += enemy_speed

    if relative_range < 1:
        relative_range = 1

    return relative_range

def get_enemy_combat_order(unit,opposing):
    if not unit.disabled:
        if "PB" == ranges[get_range_band(relative_range)]:
            attack_num = random.randint(1,10)
            if attack_num <= 5:
                unit.attack = "Fire"
            elif attack_num > 5 and attack_num <= 9:
                unit.attack = "Melee"
            elif attack_num == 10:
                unit.attack = "Charge"
                if unit.jumping:
                    if random.randint(1,10) == 10:
                        unit.attack = "DFA"
        else:
            unit.attack = "Fire"

        target_indices = []
        index = 0
        for o in opposing:
            if not o.disabled:
                target_indices.append(index)
            index += 1    

        target_index = random.randint(0,len(target_indices) - 1)
        unit.target = target_indices[target_index]
    else:
        unit.attack = "None"

def get_combat_order(unit,opposing):
    if not unit.disabled:
        # resolve all combat actions of loser of initiative then other team
        attack_choices = ["Fire","None"]
        if "PB" == ranges[get_range_band(relative_range)]:
            attack_choices.append("Melee")
            attack_choices.append("Charge")
            if unit.jumping:
                attack_choices.append("DFA")

        target_list = []
        target_indices = []
        index = 0
        for o in opposing:
            if not o.disabled:
                target_list.append(o.long_name())
                target_indices.append(index)
            index += 1
        unit.attack = get_user_input_from_list("Choose attack for " + unit.long_name() + ":",attack_choices)
        if unit.attack != "None":
            unit.target = target_indices[get_user_choice_from_list("Pick target: ",target_list)]
    else:
        unit.attack = "None"


def resolve_combat(friendlies,enemies):
    global relative_range

    range_modifier = 0
    weapon_range = 0
    range_band = get_range_band(relative_range)
    if range_band == 2:
        range_modifier = 2
        weapon_range = 1
    elif range_band == 3:
        range_modifier = 4
        weapon_range = 2
    elif range_band > 3:
        weapon_range = -1

    print("Player attacks:")
    for unit in friendlies:
        target = enemies[unit.target]
        resolve_damage(unit,target,range_modifier,weapon_range)
    print("Enemy attacks:")
    for unit in enemies:
        target = friendlies[unit.target]
        resolve_damage(unit,target,range_modifier,weapon_range)

def resolve_damage(unit,target,range_modifier,weapon_range):
    damage = 0
    to_hit = unit.skill
    to_hit += range_modifier
    to_hit += target.tmm
    if unit.jumping:
        to_hit += 2
    if target.jumping:
        to_hit += 1
    if unit.attack == "None":
        print(" * " + unit.long_name() + " doesn't attack")
        return
    if unit.attack == "Charge":
        to_hit += 1
        damage = unit.size*unit.move/8
    elif unit.attack == "DFA":
        to_hit += 3
        damage = unit.size*unit.move/8 + 1
    elif unit.attack == "Melee":
        damage = unit.size
    elif unit.attack == "Fire":
        if weapon_range < 0:
            damage = 0 # out of range
        else:
            damage = unit.damage[weapon_range]

    attack_roll = roll2d()

    print(" * " + unit.long_name() + " " + unit.attack + "s at " + target.long_name())
    print("      Target: " + str(to_hit) + " Rolled: " + str(attack_roll))

    if attack_roll >= to_hit:
        print("      Hit! for " + str(damage) + " damage.")
        target.hitpoints -= damage
        if target.hitpoints < target.structure:
            print("      Critical hit!")

        if target.hitpoints <= 0:
            print("      Destroyed!")
            target.disabled = True
    else:
        print("      Miss!")

def resolve_combat_round(friendlies,enemies):
    global relative_range

    done = False
    movement_phase = 0
    combat_phase = 0
    enemy_move_order = ""
    friendly_move_order = ""
    print("****************************************************************")
    print("****************************************************************")
    print("Enemy Units:")
    for unit in enemies:
        print("  * " + unit.long_name())
    print("Friendly Units:")
    for unit in friendlies:
        print("  * " + unit.long_name())
    print("****************************************************************")
    print("Movement Phase ...")
    enemy_turn = resolve_initiative(friendlies,enemies)
    print("Current weapons range: " + ranges[get_range_band(relative_range)])
    print("Range distance: " + str(relative_range))
    while not done:
        if enemy_turn:
            if movement_phase < 2:
                enemy_move_order = get_enemy_movement_order(enemies,friendlies)
                movement_phase += 1
                enemy_turn = False
                print("Enemy movement order: " + enemy_move_order)
            else:
                if combat_phase < 2:
                    for unit in enemies:
                        get_enemy_combat_order(unit,friendlies)
                    combat_phase += 1
                    enemy_turn = False
                else:
                    done = True
        else:
            if movement_phase < 2:
                friendly_move_order = get_movement_order(friendlies)
                movement_phase += 1
                enemy_turn = True
            else:
                if combat_phase < 2:
                    for unit in friendlies:
                        get_combat_order(unit, enemies)
                    combat_phase += 1
                    enemy_turn = True
                else:
                    done = True

        if movement_phase == 2 and combat_phase == 0:
            relative_range = resolve_movement(friendly_move_order, enemy_move_order, friendlies, enemies)
            print("****************************************************************")
            print("Combat Phase ...")
            print("Current weapons range: " + ranges[get_range_band(relative_range)])
            print("Range distance: " + str(relative_range))
        if combat_phase == 2 and not done:
            print("****************************************************************")
            #print("Enemy attacks:")
            #for unit in enemies:
            #    if not unit.disabled:
            #        print(" * " + unit.long_name() + " " + unit.attack + "s")
            resolve_combat(friendlies,enemies)


def resolve_round(friendlies,opposing):
    if resolve_initiative(friendlies,opposing):
        print("Friendlies have initiative!")
    else:
        print("Opposing side has initiative.")
    for mech in friendlies:

        movement_order = get_user_input_from_list("Select move option for " + mech.long_name() + ":",move_orders)

        jump_text = ""
        jumping = False
        if mech.jump_jets:
            if get_user_input_yes_no("Do you want to use your jump jets?"):
                jumping = True
                jump_text = " (jumping)"

        attack_order = get_user_input_from_list("Select attack option for " + mech.long_name() + ":",attacks)

        target_text = ""
        target_descs = []
        if len(opposing) > 0:
            for unit in opposing:
                target_descs.append(unit.handle + " (" + unit.designation + ")")
            target_text = get_user_input_from_list("Pick a target:",target_descs)

        print("**************************************************************")
        print(mech.handle + " will " + movement_order + jump_text +" and " + attack_order + " at " + target_text)
        print("**************************************************************")

def combat(team_one,team_two):
    gameover = False
    #resolve_round(team_one,team_two)
    while not gameover:
        resolve_combat_round(team_one,team_two)
        units_disabled = 0
        for unit in team_one:
            if unit.disabled:
                units_disabled += 1
        if units_disabled == len(team_one):
            gameover = True
            print("All friendly units destroyed. You lose.")
        units_disabled = 0
        for unit in team_two:
            if unit.disabled:
                units_disabled += 1
        if units_disabled == len(team_two):
            gameover = True
            print("All enemy units destroyed. You win!")
        if ranges[get_range_band(relative_range)] == "Disengage":
            print("Somebody fled. Battle over.")
            gameover = True

shadow_hawk = Mech({"handle":"Blue Beatle",
                    "name":"Shadow Hawk",
                    "designation":"SHD-2H",
                    "size":2,
                    "mass":55,
                    "tmm":2,
                    "move":10,
                    "jump_jets":True,
                    "damage":[2,2,1],
                    "armor":5,
                    "structure":5})

victor = Mech({"handle":"Foe Hammer",
               "name":"Victor",
               "designation":"VTR-9B",
               "size":4,
               "mass":80,
               "tmm":1,
               "move":8,
               "jump_jets":True,
               "damage":[4,4,0],
               "armor":6,
               "structure":6})

archer = Mech({"handle":"Hate Storm",
               "name":"Archer",
               "designation":"ARC-2R",
               "size":3,
               "mass":70,
               "tmm":1,
               "move":8,
               "damage":[2,3,3],
               "ov":1,
               "armor":7,
               "structure":6})

centurion = Mech({"handle":"Reaver",
                  "name":"Centurion",
                  "designation":"CN9-A",
                  "size":2,
                  "mass":50,
                  "tmm":1,
                  "move":8,
                  "damage":[2,3,1],
                  "armor":5,
                  "structure":4})


mech_1 = Mech({"handle":"Road Runner","jump_jets":True})
mech_2 = Mech({"handle":"Ostrich"})
mech_3 = Mech({"handle":"Glory Bird"})
mech_4 = Mech({"handle":"Seriously?"})
team_one = [mech_1,mech_2]
team_two = [mech_3,mech_4]
team_three = [archer,centurion]
team_four = [shadow_hawk,victor]
#combat(team_one,team_two)
combat(team_four,team_three)