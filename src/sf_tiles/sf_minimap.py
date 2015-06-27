from sf_tiles.sf_tile import Tile

class Minimap(Tile):
    def __init__(self):
        Tile.__init__(self, (200, 200, 200), (0, 0, 1024, 100))
