class Duct(dict):
    '''
    duck = Duct(voice = "quack", mass = 0.6)
    assert duck.voice, "quack"
    duck.spam = "ham"
    '''

    def __getattr__(self, k):
        return self[k]

    def __setattr__(self, k, v):
        self[k] = v


Colors = Duct(
    white=(255, 255, 255),
    light_gray=(200, 200, 200),
    gray=(150, 150, 150)
)
