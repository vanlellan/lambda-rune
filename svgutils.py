import numpy as np

class SVG(object):
    def __init__(self, outfile, width, height):
        self.outfile = outfile
        self.width = width
        self.height = height
        self.lines = []
        self.lines.append('<svg width="{}" height="{}">\n'.format(self.width, self.height))
        self.lines.append('<rect fill="white" stroke="black" x="0" y="0" width="{}" height="{}" />\n'.format(self.width, self.height))
        self.center = (self.width/2, self.height/2)

    def Circ(self, cx, cy, r, sw):
        self.lines.append('<circle cx="{}" cy="{}" r="{}" stroke-width="{}" stroke="black" fill="white"/>\n'.format(cx, cy, r, sw))

    def Poly(self, nodes, sw):
        ptstr = " ".join(["{},{}".format(n.cx, n.cy) for n in nodes])
        self.lines.append('<polygon points="{}" fill="none" stroke="black" stroke-width="{}"/>\n'.format(ptstr, sw))

    def Arc(self, nodeA, nodeB, sw, flip=False):
        d = np.sqrt((nodeB.cx - nodeA.cx)**2 + (nodeB.cy - nodeA.cy)**2)
        self.lines.append('<path d="M {} {} A {} {} 0 0 {} {} {}" stroke-width="{}" stroke="black" fill="none"/>\n'.format(nodeA.cx, nodeA.cy, d, d, int(flip), nodeB.cx, nodeB.cy, sw))

    def write(self):
        with open(self.outfile, 'w') as f:
            for line in self.lines:
                f.write(line)
            f.write('</svg>')

if __name__ == "__main__":
    pass
