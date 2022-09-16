import numpy as np
from util import parse
import pdb
# PRED := λn.λf.λx.n (λg.λh.h (g f)) (λu.x) (λu.u)
# Lnfx.n Lgh.h(gf) Lu.x Lu.u


class NodeRing(object):
    def __init__(self, cx, cy, r, expression, offset=False, start_ang=0.):
        self.cx = cx
        self.cy = cy
        self.r = r
        self.expression = expression
        self.offset = offset
        self.start_ang = start_ang
        self.nodes = []
        self.parseExpression()
        self.links = []
        self.parentheses = []

    def parseExpression(self):
        # Parse text in expression
        if "L" in self.expression: # Head
            variables = list(self.expression)
        else:
            variables = self.expression

        # Allocate nodes based on variables
        nodes = []
        for i, var in enumerate(variables):
            ang = self.start_ang - np.pi/2 + i*2*np.pi/len(variables)
            if self.offset:
                ang += np.pi / len(variables)
            nodes.append(Node(ang, self.r, self, var))
        self.nodes = nodes

    def parseParentheses(self): # TODO: Change to nested lists
        # Creates parentheses using linked pairs of ghost nodes
#        resolver = self.expression
#        while ('(' in resolver or ')' in resolver):
#            inner, l, r = unnest(resolver)
#            argmap = mapinds(resolver)
#            resolver = resolver.replace("({})".format(inner), inner)
#            self.parentheses.append((self.nodes[argmap[l]].before, self.nodes[argmap[r]].after))
        pass

    def linkToOther(self, other):
        # Creates variable arcs using linked pairs of nodes
        for self_node in self.nodes:
            for other_node in other.nodes:
                if (self_node.expression == other_node.expression and self_node.expression != "L"):
                    self.links.append((self_node, other_node))
        return self.links


class Node(object):
    def __init__(self, th, r, parent, expression):
        self.th = th
        self.r = r
        self.parent = parent
        self.expression = expression

        self.after = GhostNode(th+15*np.pi/180, self.r, self.parent)
        self.before = GhostNode(th-15*np.pi/180, self.r, self.parent)

        self.calculateXY()
        self.parseExpression()

    def calculateXY(self):
        self.cx = self.parent.cx + self.r * np.cos(self.th)
        self.cy = self.parent.cy + self.r * np.sin(self.th)

    def parseExpression(self):
        if type(self.expression) == str:
            self.content = None
        else:
            self.content = Rune(self.cx, self.cy, self.r/2, self.expression, start_ang=self.th+np.pi/2)

    def draw(self, svg):
        if self.content == None:
            pass
        else:
            self.content.draw(svg)


class GhostNode(Node):
    def __init__(self, th, r, parent):
        self.th = th
        self.r = r
        self.parent = parent
        self.calculateXY()


class Head(NodeRing):
    def draw(self, svg):
        svg.Circ(self.cx, self.cy, self.r, 3) # Head circ
        if len(self.nodes) == 2:
            svg.Circ(self.nodes[1].cx, self.nodes[1].cy, 2.5, 5)
        else:
            svg.Poly(self.nodes, 1) # Inscribed polygon
        svg.Circ(self.nodes[0].cx, self.nodes[0].cy, 10, 3) # Start node circ


class Body(NodeRing):
    def __init__(self, cx, cy, r, expression, start_ang=0.):
        NodeRing.__init__(self, cx, cy, r, expression, offset=True, start_ang=start_ang)
        self.parseParentheses()

    def draw(self, svg):
        svg.Circ(self.cx, self.cy, self.r, 3) # Body circ
        if len(self.nodes) == 1:
            svg.Circ(self.nodes[0].cx, self.nodes[0].cy, 2.5, 5)
        svg.Poly(self.nodes, 1) # Inscribed polygon


class Rune(object):
    def __init__(self, cx, cy, r, expression, start_ang=0.):
        self.cx = cx
        self.cy = cy
        self.r = r
        self.expression = expression
        self.start_ang = start_ang

        self.head = Head(self.cx, self.cy, self.r, self.expression[0], start_ang=self.start_ang)
        if len(self.head.nodes) <= 2:
            apothem = 0.7*self.r
        else:
            apothem = self.r * np.cos(np.pi / len(self.head.nodes))/1.25
        self.body = Body(self.cx, self.cy, apothem, self.expression[1], start_ang=self.start_ang)

        self.head.linkToOther(self.body)
        for node in self.body.nodes:
            if node.content is not None:
                self.head.linkToOther(node.content.body)

    def draw(self, svg):
        self.head.draw(svg)
        self.body.draw(svg)
        for parenthesis in self.body.parentheses:
            svg.Arc(*parenthesis, 1)
        for node in self.body.nodes:
            node.draw(svg)
        for link in self.head.links:
            flip = True
            midpoint = (0.5*(link[1].cx+link[0].cx), 0.5*(link[1].cy+link[0].cy))
            distance = np.sqrt((link[1].cx - link[0].cx)**2 + (link[1].cy - link[0].cy)**2)
            curvature = distance / self.r
            if midpoint[0] > self.cx and midpoint[1] < self.cy:
                flip = False
            if len(self.head.nodes)==2 and len(self.body.nodes)==1:
                svg.Poly(link, 3)
            else:
                svg.Arc(*link, 3, flip=flip, curvature=curvature)


if __name__ == "__main__":
    import argparse
    import subprocess
    import platform
    from util import parse
    from svgutils import SVG

    # Parse command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('expression', type=str)
    parser.add_argument('-o', '--outfile', type=str, default='myrune.svg')
    args = parser.parse_args()

    # Create SVG canvas, render rune, write out the file
    svg = SVG(args.outfile, 800, 800)
    rune = Rune(400, 400, 250, parse(args.expression))
    rune.draw(svg)
    svg.write()

    # Open the saved SVG file from the command line to display the image
    if platform.system() == "Windows":
        import os
        os.startfile(args.outfile)
    elif platform.system() == "Darwin":
        subprocess.run("open {}".format(args.outfile).split())
    else:
        subprocess.run("gio open {}".format(args.outfile).split())
        
