import numpy as np
# PRED := λn.λf.λx.n (λg.λh.h (g f)) (λu.x) (λu.u)
# Lnfx.n Lgh.h(gf) Lu.x Lu.u

class NodeRing(object):
    def __init__(self, cx, cy, r, expression):
        self.cx = cx
        self.cy = cy
        self.r = r
        self.expression = expression
        self.nodes = []
        self.parseExpression()

    def parseExpression(self):
        chars = list(self.expression)
        nodes = []
        for i, char in enumerate(chars):
            ang = -np.pi/2 + i*2*np.pi/len(chars)
            nodes.append(Node(ang, self.r, self, char))
        self.nodes = nodes


class Node(object):
    def __init__(self, th, r, parent, expression):
        self.th = th
        self.r = r
        self.parent = parent
        self.cx = parent.cx + self.r * np.cos(self.th)
        self.cy = parent.cy + self.r * np.sin(self.th)
        self.expression = expression


class Head(NodeRing):
    def draw(self, svg):
        svg.Circ(self.cx, self.cy, self.r, 2) # Head circ
        svg.Poly(self.nodes, 1) # Inscribed polygon
        svg.Circ(self.nodes[0].cx, self.nodes[0].cy, 10, 2) # Start node circ


class Body(NodeRing):
    def draw(self, svg):
        svg.Circ(self.cx, self.cy, self.r, 2) # Body circ
        svg.Poly(self.nodes, 1) # Inscribed polygon


class Rune(object):
    def __init__(self, svg, cx, cy, r, expression):
        self.svg = svg
        self.cx = cx
        self.cy = cy
        self.r = r
        self.expression = expression

        self.head = Head(self.cx, self.cy, self.r, expression.split('.')[0])
        apothem = self.r * np.cos(np.pi / len(self.head.nodes))
        self.body = Body(self.cx, self.cy, apothem, expression.split('.')[1])

    def draw(self):
        self.head.draw(self.svg)
        self.body.draw(self.svg)


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

    def write(self):
        with open(self.outfile, 'w') as f:
            for line in self.lines:
                f.write(line)
            f.write('</svg>')

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('expression', type=str)

    args = parser.parse_args()

    svg = SVG('test.svg', 400, 400)
    rune = Rune(svg, 200, 200, 150, args.expression)
    rune.draw()
    svg.write()
