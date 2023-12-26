from src.audio.MusicHandler import MusicHandler
from src.audio.SfxHandler import SfxHandler


class AudioHandlerFactory:
    def __init__(self):
        pass

    def create_handler(self, component_id, *args, **kwargs):
        if component_id.lower() == "musichandler":
            return MusicHandler(*args, **kwargs)
        elif component_id.lower() == "sfxhandler":
            return SfxHandler(*args, **kwargs)