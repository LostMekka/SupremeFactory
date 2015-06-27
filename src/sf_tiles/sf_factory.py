from sf_tiles.sf_tile import Tile

class Factory(Tile):
    def __init__(self):
        Tile.__init__(self, (255, 255, 255), (0, 100, 400, 600))

