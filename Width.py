class Width:
    def __init__(self, sOffset, a, b, c, d):
        self.sOffset = sOffset
        self.a = a
        self.b = b
        self.c = c
        self.d = d

    def printWidth(self, level):
        return level * "    " + f'<width sOffset="{self.sOffset}" a="{self.a}" b="{self.b}" c="{self.c}" d="{self.d}"/>\n'
