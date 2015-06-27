from utils import Duct, Colors

factory_tile = Duct(bg_color=Colors.white, rect=(0, 100, 400, 600))
minimap_tile = Duct(bg_color=Colors.light_gray, rect=(0, 0, 1024, 100))
battlefield_tile = Duct(bg_color=Colors.gray, rect=(400, 100, 624, 600))

tiles = [
    factory_tile,
    minimap_tile,
    battlefield_tile
]
