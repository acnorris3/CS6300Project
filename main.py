# main.py
from simulation.unifiedUI import UnifiedUI
from simulation.menuScreen import menuScreen
from simulation.pip_example_tiles import PIP_Example_Tiles

UnifiedUI(game_instance=PIP_Example_Tiles, menu_instance=menuScreen).main_loop()