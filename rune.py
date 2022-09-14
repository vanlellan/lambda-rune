import numpy as np
from util import unnest, mapinds
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
        self.parentheses = []

    def parseExpression(self):
        justvars = "".join([l for l in self.expression if l not in ['(', ')']])
        chars = list(justvars)
        nodes = []
        for i, char in enumerate(chars):
            ang = -np.pi/2 + i*2*np.pi/len(chars)
            nodes.append(Node(ang, self.r, self, char))
        self.nodes = nodes

    def parseParentheses(self):
        resolver = self.expression
        while ('(' in resolver or ')' in resolver):
            inner, l, r = unnest(resolver)
            argmap = mapinds(resolver)
            resolver = resolver.replace("({})".format(inner), inner)
            self.parentheses.append((self.nodes[argmap[l]].before, self.nodes[argmap[r]].after))


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

        self.after = GhostNode(th+15*np.pi/180, self.r, self.parent)
        self.before = GhostNode(th-15*np.pi/180, self.r, self.parent)

    def calculateXY(self):
        self.cx = self.parent.cx + self.r * np.cos(self.th)
        self.cy = self.parent.cy + self.r * np.sin(self.th)


class GhostNode(Node):
    def __init__(self, th, r, parent):
        self.th = th
        self.r = r
        self.parent = parent
        self.calculateXY()


class Head(NodeRing):
    def draw(self, svg):
        svg.Circ(self.cx, self.cy, self.r, 3) # Head circ
        svg.Poly(self.nodes, 1) # Inscribed polygon
        svg.Circ(self.nodes[0].cx, self.nodes[0].cy, 10, 3) # Start node circ


class Body(NodeRing):
    def __init__(self, cx, cy, r, expression, offset=False):
        NodeRing.__init__(self, cx, cy, r, expression)
        if offset:
            for node in self.nodes:
                node.th += np.pi / len(self.nodes)
                node.calculateXY()
                node.after.th += np.pi / len(self.nodes)
                node.after.calculateXY()
                node.before.th += np.pi / len(self.nodes)
                node.before.calculateXY()
        self.parseParentheses()

    def draw(self, svg):
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
        self.body = Body(self.cx, self.cy, apothem, expression.split('.')[1], offset=True)

        self.head.linkToOther(self.body)

    def draw(self):
        self.head.draw(self.svg)
        self.body.draw(self.svg)
        for link in self.head.links:
            # if (some condition regarding the position of nodes)
            #     set curvature, flip parameters to optimize position
            self.svg.Arc(*link, 3, flip=True)
        for parenthesis in self.body.parentheses:
            self.svg.Arc(*parenthesis, 1)


if __name__ == "__main__":
    import argparse
    import subprocess
    import platform
    from svgutils import SVG

    # Parse command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('expression', type=str)
    args = parser.parse_args()

    # Create SVG canvas, render rune, write out the file
    svg = SVG('{}.svg'.format(args.expression), 400, 400)
    rune = Rune(svg, 200, 200, 150, args.expression)
    rune.draw()
    svg.write()

    # Open the saved SVG file from the command line to display the image
    if platform.system() == "Windows":
        import os
        os.startfile("{}.svg".format(args.expression).split())
    elif platform.system() == "Darwin":
        subprocess.run("open {}.svg".format(args.expression).split())
    else:
        subprocess.run("xdg-open {}.svg".format(args.expression).split())
        
