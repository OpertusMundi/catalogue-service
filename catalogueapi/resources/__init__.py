import os

def base_dir():
    '''The base directory that can be used to resolve ref resources'''
    return os.path.dirname(__file__) + "/"
