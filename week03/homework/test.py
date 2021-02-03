import sys


class systemInfo:
    ''' 
    Simple SystemInfo Class that obtains
    the major python version and the
    operating system type
    '''

    def __init__(self):
        ''' Create object variables and Constants '''
        self.OS = sys.platform


obj = systemInfo()
print(obj.OS)
