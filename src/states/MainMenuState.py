from src.states.StateBase import StateBase


class MainMenuState(StateBase):
    def __init__(self, game, GUIFactory):
        super().__init__(game, GUIFactory)

    def initialise_gui(self):
        self._gui = [
            {
            "options_button": self._GUIFactory.create_gui("TextButton", self._game.window, self.options_button_click, self._game.audiohandler, text="Options"),
            "exit_button": self._GUIFactory.create_gui("TextButton", self._game.window, self.exit_button_click, self._game.audiohandler, text="Exit"),
            "play_button": self._GUIFactory.create_gui("TextButton", self._game.window, self.play_button_click, self._game.audiohandler, text="Play"),
            "logo": self._GUIFactory.create_gui("TextLabel", self._game.window, has_box=False, has_outline=False, font_size=100, text="BlockBuild!", font_name="bahnschrift")
            },
            {},
            {}
        ]

    def on_state_enter(self, *args):
        self._game.audiohandler.set_shuffle_list([])
        if self._game.previous_state is not self._game.states["main_menu"]:
            self._game.audiohandler.shuffle_play()

        self._gui[0]["play_button"].size = (400.0, 75.0)
        self._gui[0]["options_button"].size = (400.0, 75.0)
        self._gui[0]["exit_button"].size = (400.0, 75.0)

        self._gui[0]["play_button"].font_size = 45
        self._gui[0]["options_button"].font_size = 45
        self._gui[0]["exit_button"].font_size = 45

        self._gui[0]["play_button"].centre_position = (600.0, 300.0)
        self._gui[0]["options_button"].centre_position = (600.0, 400.0)
        self._gui[0]["exit_button"].centre_position = (600.0, 500.0)

        self._gui[0]["logo"].centre_position = (600.0, 100.0)

        #self._gui["play_button"].is_enabled = False

    def on_state_leave(self, *args):
        pass

    def update(self):
        self._game.window.fill((255, 255, 255))
        for layer in self._gui[::-1]:
            for component in layer.values():  # Iterates through all guis in dict and updates and draws them
                component.update()
                component.draw()

    def options_button_click(self, button):
        self._game.push_state("options_menu")

    def play_button_click(self, button):
        self._game.push_state("load_game_menu")

    def exit_button_click(self, button):
        self._game.pop_state()
