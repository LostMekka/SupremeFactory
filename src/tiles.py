from utils import Duct, Colors


def create_ui():
    base_factory_tile = Duct(bg_color=Colors.dark_gray, rect=(0, 100, 400, 600))
    minimap_tile = Duct(bg_color=Colors.light_gray, rect=(0, 0, 1024, 100))
    visionrect_tile = Duct(bg_color=Colors.white, rect=(5, 5, 140, 90))
    battlefield_tile = Duct(bg_color=Colors.gray, rect=(400, 100, 624, 600))

    return [
        base_factory_tile,
        minimap_tile,
        visionrect_tile,
        battlefield_tile
    ]
