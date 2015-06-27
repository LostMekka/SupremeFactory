from sf_tiles.sf_tile import Tile

class Battlefield(Tile):
    def __init__(self):
        Tile.__init__(self, (150, 150, 150), (400, 100, 624, 600))
