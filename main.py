# main.py
import simulation.menuScreen
from mower.mower import Mower
from simulation.simulationEngine import simulationEngine

this_mower = Mower()
this_simulation = simulationEngine()
this_main_screen = simulation.menuScreen.menuScreen()
this_main_screen.run_menu_screen_loop()