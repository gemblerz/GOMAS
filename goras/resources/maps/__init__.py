import os

def get_maps():
    path = os.path.dirname(os.path.realpath(__file__))
    files = os.listdir(path)
    return [os.path.join(path, x) for x in files if 'SC2Map' in x]

goras_maps = get_maps()