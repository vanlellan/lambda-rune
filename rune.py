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
        self.links = []

    def parseExpression(self):
        chars = list(self.expression)
        nodes = []
        for i, char in enumerate(chars):
            ang = -np.pi/2 + i*2*np.pi/len(chars)
            nodes.append(Node(ang, self.r, self, char))
        self.nodes = nodes

    def linkToOther(self, other):
        for self_node in self.nodes:
            for other_node in other.nodes:
                if self_node.expression == other_node.expression:
                    self.links.append((self_node, other_node))
        return self.links


class Node(object):
    def __init__(self, th, r, parent, expression):
        self.th = th
        self.r = r
        self.parent = parent
        self.expression = expression
        self.calculateXY()

    def calculateXY(self):
        self.cx = self.parent.cx + self.r * np.cos(self.th)
        self.cy = self.parent.cy + self.r * np.sin(self.th)


class Head(NodeRing):
    def draw(self, svg):
        svg.Circ(self.cx, self.cy, self.r, 3) # Head circ
        svg.Poly(self.nodes, 1) # Inscribed polygon
        svg.Circ(self.nodes[0].cx, self.nodes[0].cy, 10, 3) # Start node circ


class Body(NodeRing):
    def draw(self, svg, offset=False):
        if offset:
            for node in self.nodes:
                node.th += np.pi / len(self.nodes)
                node.calculateXY()
        svg.Circ(self.cx, self.cy, self.r, 3) # Body circ
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

        self.links = self.head.linkToOther(self.body)

    def draw(self):
        self.head.draw(self.svg)
        self.body.draw(self.svg, offset=True)
        for link in self.links:
            self.svg.Arc(*link, 3, flip=True)
#            self.svg.Arc(*link, 3)


if __name__ == "__main__":
    import argparse
    import subprocess
    import time
    from svgutils import SVG

    parser = argparse.ArgumentParser()
    parser.add_argument('expression', type=str)

    args = parser.parse_args()

    svg = SVG('{}.svg'.format(args.expression), 400, 400)
    rune = Rune(svg, 200, 200, 150, args.expression)
    rune.draw()
    svg.write()

    subprocess.run("gio open {}.svg".format(args.expression).split())
