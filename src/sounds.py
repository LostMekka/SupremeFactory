from pygame.mixer import Sound
import random
import config


def cached(f):
    def ff():
        try:
            return f.cache
        except:
            f.cache = f()
            return f.cache
    return ff


@cached
def load_piu():
    return Sound(file = "./assets/piu.ogg")

@cached
def load_arghs():
    paths = ["./assets/argh"+str(i)+".ogg" for i in range(1,6)]
    return [Sound(file = path) for path in paths]

def play_piu():
    if config.sounds:
        load_piu().play()

def play_argh():
    if config.sounds:
        random.sample(load_arghs(), 1)[0].play()
