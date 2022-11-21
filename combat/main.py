import ui
import scene
import actor
import mechs


current_scene = scene.CombatScene()

def start():
    ui.initialize_screen("Yo! It's combat!")
    while 1:
        user_input = ui.process_user_input()
        current_scene.run(user_input)
        ui.update_screen()

start()