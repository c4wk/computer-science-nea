import pygame
import json

from states.MainMenuState import MainMenuState
from states.LoadGameMenuState import LoadGameMenuState
from states.OptionsMenuState import OptionsMenuState

from src.sprite.Spritesheet import Spritesheet

from base.Game import Game

from src.factories.GUIFactory import GUIFactory
from states.StateStack import StateStack

from src.factories.BlockFactory import BlockFactory

from src.world.Camera import Camera
from src.world.RegionGenerator import RegionGenerator
from src.world.World import World

from src.audio.MusicHandler import MusicHandler
from src.audio.SfxHandler import SfxHandler

from states.MainGameState import MainGameState


def main():
    pygame.init()
    state_stack = StateStack()  # Holds different "states" which have their own game loops.
    clock = pygame.time.Clock()

    config = None
    with open("config.json") as f:
        config = json.load(f)

    window = pygame.display.set_mode((config["window_size_x"], config["window_size_y"]))
    pygame.display.set_caption(config["window_caption"])

    gui_factory = GUIFactory()
    block_factory = BlockFactory(config["blocks"],
                                 Spritesheet("../assets/imgs/sprites/block_textures/block_textures.png",
                                             "../assets/imgs/sprites/block_textures/block_textures.json"))

    region_generator = RegionGenerator()
    camera = Camera()
    music_handler = MusicHandler(250, False)
    sfx_handler = SfxHandler()

    game = Game(state_stack, window, clock, music_handler, sfx_handler,
                config["framerate"], config, gui_factory,\
                block_factory)  # Game class handles overall running of game
    world = World(game, camera, region_generator)

    game.add_to_states("main_menu", MainMenuState(game))
    game.add_to_states("options_menu", OptionsMenuState(game))
    game.add_to_states("load_game_menu", LoadGameMenuState(game))
    game.add_to_states("main_game", MainGameState(game, world))
    game.game_loop()


if __name__ == "__main__":
    main()

