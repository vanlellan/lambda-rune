
#accept a lambda-calculus expression from the command line
#output minimalist linear rune SVGs of that expression

#with this version, let's try accommodating one level of internal lambda expressions
#let me first enclose all internal lambda expressions with []

#NOTES:
    #all lambdas ("L") must be immediately preceded by an opening square bracket "["
    #a closing square bracket "]" delineates the end of the body of that lambda expression
import sys

class lambdaExpression:

    def __init__(self, string):
        self.string = string
        self.checkExpression(string)
        self.head, predicate = self.string[2:-1].split(".", 1)
        if " " in predicate:
            self.body, self.arg = predicate.split(" ")
        else:
            self.body = predicate
            self.arg = ""
        print("head = ", self.head)
        print("body = ", self.body)
        print("arg  = ", self.arg)

        self.listifyBody()
        print("BODY LIST = ", self.bodyList)

        self.headcount = len(self.head)
        self.bodyclean = self.body.replace("(","").replace(")","")
        self.bodycount = len(self.bodyclean)

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

    def listifyBody(self):
        self.bodyList = []
        braOpen = False
        for i,s in enumerate(self.body):
            if braOpen:
                self.bodyList[-1] += s
            else:
                if s == "[":
                    braOpen = True
                    self.bodyList.append(s)
                elif s == "]":
                    braOpen = False
                    self.bodyList[-1] += s
                else:
                    self.bodyList.append(s)

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
lamEx = lambdaExpression(lamex)

width = 100*max(lamEx.headcount+1, lamEx.bodycount+1)
height = 300

staves = [(0, height/3, width, height/3), (0, 2*height/3, width, 2*height/3)]

headSpace = width/(lamEx.headcount+1)
bodySpace = width/(lamEx.bodycount+1)

dots = []
for i in range(lamEx.headcount):
    dots.append(((i+1)*headSpace,height/3))
for i in range(lamEx.bodycount):
    dots.append(((i+1)*bodySpace,2*height/3))

lines = []
for i,a in enumerate(lamEx.head):
    for b in lamEx.bodymatch[i]:
        lines.append(((i+1)*headSpace,height/3,(b+1)*bodySpace,2*height/3))

curves = []
for i in lamEx.pairs:
    curves.append(((i[0]+1)*bodySpace, 2*height/3,(i[1]+1)*bodySpace, 2*height/3))

with open("output.svg","w") as f:
    f.write(f"<svg width=\"{width}\" height=\"{height}\" viewBox=\"0 0 {width} {height}\">")
    f.write(f"<rect fill=\"white\" stroke=\"black\" x=\"0\" y=\"0\" width=\"{width}\" height=\"{height}\"/>")
    for a in staves:
        f.write(f"<path d=\"M {a[0]} {a[1]} L {a[2]} {a[3]}\" stroke-width=\"4\" stroke=\"black\" />")
    for a in lines:
        f.write(f"<path d=\"M {a[0]} {a[1]} L {a[2]} {a[3]}\" stroke-width=\"4\" stroke=\"black\" />")
    for a in curves:
        f.write(f"<path d=\"M {a[0]} {a[1]} C {a[0]} {a[1]+0.25*(a[2]-a[0])} {a[2]} {a[3]+0.25*(a[2]-a[0])} {a[2]} {a[3]}\" stroke-width=\"4\" stroke=\"black\" fill-opacity=\"0\" />")
    for a in dots:
        f.write(f"<circle cx=\"{a[0]}\" cy=\"{a[1]}\" r=\"10\" fill=\"black\" />")
    f.write(f"</svg>")
