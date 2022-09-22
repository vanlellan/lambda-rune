
#accept a lambda-calculus expression from the command line
#output minimalist linear rune SVGs of that expression

#with this version, let's try accommodating one level of internal lambda expressions
#let me first enclose all internal lambda expressions with []

#NOTES:
    #all lambdas ("L") must be immediately preceded by an opening square bracket "["
    #a closing square bracket "]" delineates the end of the body of that lambda expression
import sys

maxDepth = 0

def listify(aString, body=False, currentDepth=1):
    newList = []
    braOpen = 0
    for i,s in enumerate(aString):
        if braOpen == 0:
            newList.append(s)
        else:
            newList[-1] += s
        if s == "[":
            braOpen += 1
        if s == "]":
            braOpen -= 1
    if body:
        for j,e in enumerate(newList):
            if len(e) > 1:
                newList[j] = lambdaExpression(e, currentDepth+1, j)
    return newList

class lambdaExpression:
    #assume that the input string represents a single, outer lambda expression
    def __init__(self, string, depth, outerIndex):
        self.string = string
        self.depth = depth
        self.outerIndex = outerIndex
        print(f"outerIndex = {outerIndex}")
        global maxDepth
        maxDepth = max(maxDepth, self.depth)
        self.checkExpression(string)
        self.head, self.body = self.string[2:-1].split(".", 1)
        print("head = ", self.head)
        print("body = ", self.body)

        self.headList = list(self.head)
        self.bodyList = listify(self.body, body=True, currentDepth=self.depth)
        print("BODY LIST = ", self.bodyList)
        #HOLY ONE-LINER, BATMAN
        self.bodyListClean = list(filter(lambda a: a not in "()" if isinstance(a, str) else True, self.bodyList))
        print(f"bodyListClean = {self.bodyListClean}")

        #calculate self.totalWidth
            #this should be max of head and body with, in node count, accounting for width of all sub-expressions in the body
        #self.totalWidth = ---recursive getWidth call goes here---

        self.headcount = len(self.head)
        self.bodyclean = self.body.replace("(","").replace(")","")
        self.bodycount = len(self.bodyListClean)

        self.bodymatch = []
        for a in self.head:
            self.bodymatch.append([j for j,x in enumerate(self.bodyclean) if x==a])

        pars = []
        for i,s in enumerate(self.body):
            if s == "(":
                pars.append(["open", i])
            elif s == ")":
                pars.append(["close",i])
        #shift par indices to their corresponding symbols
        for i,a in enumerate(pars):
            if a[0] == "open":
                a[1] -= i
            elif a[0] == "close":
                a[1] -= i+1
        
        #pair paren endpoints together
        self.pairs = []
        while len(pars) > 0:
            for j,p in enumerate(pars):
                if p[0] == "close":
                    print("j = ", j)
                    print("pars = ", pars)
                    self.pairs.append((pars[j-1][1],p[1]))
                    pars = pars[:j-1]+pars[j+1:]
                    break
                else:
                    pass

    def __str__(self):
        return f"L{self.headList}.{self.bodyList}"

    def __repr__(self):
        return f"L{self.headList}.{self.bodyList}"

    def checkExpression(self, aExp):
        if aExp[:2] != "[L":
            print("Invalid lambda expression syntax: must start with \"[L\".")
            sys.exit(1)
        if "." not in aExp:
            print("Invalid lambda expression syntax: must contain '.'")
            sys.exit(1)
        if aExp[-1] != "]":
            print("Invalid lambda expression syntax: must end with \"]\".")
            sys.exit(1)

lamex = sys.argv[1]
masterList = listify(lamex)
print("masterList = ", masterList)
masterList = [lambdaExpression(a,1,i) for i,a in enumerate(masterList)]  #assume outer expression is concatenation of lambda expressions
print("masterList = ", masterList)
print(f"maxDepth = {maxDepth}")

concatSep = 10
xstart = concatSep
with open("output.svg","w") as f:
    totalWidth = 100*sum([max(l.headcount+1, l.bodycount+1) for l in masterList])+concatSep*(len(masterList)+1)
    height = 300
    ystart = height/2
    f.write(f"<svg width=\"{totalWidth}\" height=\"{height}\" viewBox=\"0 0 {totalWidth} {height}\">")
    f.write(f"<rect fill=\"white\" stroke=\"black\" x=\"0\" y=\"0\" width=\"{totalWidth}\" height=\"{height}\"/>")
    colorList = ["black", "black", "black", "red", "orange", "green", "blue"]
    #need to replace this for loop with an element-by-element walk through masterList, drawing each element as we get to it
        #build a node-dict during the walk (key:letter, value:(x,y)), and check the entire dict at each new node to draw connections
        #start with a horizontal line
            #draw method reads in starting position and outputs svg code with absolute positions
                #depends on starting position, depth, totalWidth, head, body
    for j,lamEx in enumerate(masterList):
        
        myColor = colorList[j]

        width = 100*max(lamEx.headcount+1, lamEx.bodycount+1)

        staves = [(xstart, height/3, xstart+width, height/3), (xstart, 2*height/3, xstart+width, 2*height/3)]
        
        headSpace = width/(lamEx.headcount+1)
        bodySpace = width/(lamEx.bodycount+1)
        
        dots = []
        for i in range(lamEx.headcount):
            dots.append((xstart+(i+1)*headSpace,height/3))
        for i in range(lamEx.bodycount):
            dots.append((xstart+(i+1)*bodySpace,2*height/3))
        
        lines = []
        for i,a in enumerate(lamEx.head):
            for b in lamEx.bodymatch[i]:
                lines.append((xstart+(i+1)*headSpace,height/3,xstart+(b+1)*bodySpace,2*height/3))
        
        curves = []
        for i in lamEx.pairs:
            curves.append((xstart+(i[0]+1)*bodySpace, 2*height/3,xstart+(i[1]+1)*bodySpace, 2*height/3))
       
        #f.write(f"<path d=\"M {xstart} {20} L {xstart} {height-20}\" stroke-width=\"2\" stroke=\"{myColor}\" />")
        f.write(f"<path d=\"M {xstart-concatSep} {ystart} L {xstart} {ystart}\" stroke-width=\"4\" stroke=\"{myColor}\" />")
        f.write(f"<path d=\"M {xstart+width} {ystart} L {xstart+width+concatSep} {ystart}\" stroke-width=\"4\" stroke=\"{myColor}\" />")
        f.write(f"<path d=\"M {xstart} {ystart+height/6} L {xstart} {ystart-height/6}\" stroke-width=\"4\" stroke=\"{myColor}\" />")
        f.write(f"<path d=\"M {xstart+width} {ystart+height/6} L {xstart+width} {ystart-height/6}\" stroke-width=\"4\" stroke=\"{myColor}\" />")
        for a in staves:
            f.write(f"<path d=\"M {a[0]} {a[1]} L {a[2]} {a[3]}\" stroke-width=\"4\" stroke=\"{myColor}\" />")
        for a in lines:
            f.write(f"<path d=\"M {a[0]} {a[1]} L {a[2]} {a[3]}\" stroke-width=\"4\" stroke=\"{myColor}\" />")
        for a in curves:
            f.write(f"<path d=\"M {a[0]} {a[1]} C {a[0]} {a[1]+0.25*(a[2]-a[0])} {a[2]} {a[3]+0.25*(a[2]-a[0])} {a[2]} {a[3]}\" stroke-width=\"4\" stroke=\"{myColor}\" fill-opacity=\"0\" />")
        for a in dots:
            f.write(f"<circle cx=\"{a[0]}\" cy=\"{a[1]}\" r=\"10\" fill=\"{myColor}\" />")
        xstart += width+concatSep

    f.write(f"</svg>")
