'''
Help functions and classes for the Quadtree
'''

class Interest:
    def __init__(self, xmin, ymin, xmax, ymax):
        self.xmin = xmin
        self.ymin = ymin
        self.xmax = xmax
        self.ymax = ymax

    def clip(self, tree):
        self.xmin = min(self.xmin)
        self.ymin = min(self.ymin)
        self.xmax = max(self.xmax)
        self.ymax = max(self.ymax)

class Nearest:
    def __init__(self):
        self.source = None
        self.dist = None

class memoize:
    def __init__(self, function):
        self.function = function
        self.memoized = {}

    def __call__(self, *args):
        try:
            return self.memoized[args]
        except KeyError:
            self.memoized[args] = self.function(*args)
            return self.memoized[args]
