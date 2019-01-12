# literallelrin elemanlarinin orderlari problem



nextname = 0
base = []
goal = []
deriv = {}
deriv_n = []
use = {}
use_n = {}
lc = -1

class literal:
    def __init__(self, name, lvar, lfunc, lcons, lneg, lmap):
        self.name = name
        self.var = lvar
        self.func = lfunc
        self.cons = lcons
        self.neg  = lneg
        self.map = lmap

class function:
    def __init__(self, name, lvar, lcons, lfunc):
        self.name = name
        self.var = lvar
        self.cons = lcons
        self.func = lfunc

def printFunc(f):
    print "func name",f.name,
    for i in f.var:
        print "func vars",i,
    for i in f.cons:
        print "func cons",i,
    for i in f.func:
        printFunc(i)

def printLiteral(lit):
    if(lit.neg == True):
        print "neg",
    print "literal name ",lit.name,
    for i in lit.var:
        print "vars",i,
    for i in lit.cons:
        print "cons",i,
    for i in lit.func:
        printFunc(i)
    print

def funcHandle(el):
    fname = el[0]
    funcV = []
    funcC = []
    funcF = []
    new = el[2:-1]
    #print new
    splited = new.split(",")
    splited = splitedFix(splited)
    #print splited
    for i in splited:
        if i != "":
            if (i[0].islower() == True):
                #print i
                if len(i)==1:

                    funcV.append(i[0])
                else:
                    temp = funcHandle(i)
                    funcF.append(temp)

            else:
                funcC.append(i[0])

    result = function(fname,funcV,funcC,funcF)
    return result

def splitedFix(splited):
    #print splited
    news = []
    hold = ""
    count = 0
    for i in splited:
        count += i.count("(")
        count -= i.count(")")
        if count == 0:
            hold = hold+i
            news.append(hold)
            hold = ""
        else:
            hold =hold+ i+","
    #print news
    return news

def parser(changed,loc,b_g):
    global base
    global goal
    neg = False
    var = []
    func = []
    cons = []
    maps = {}
    changed = changed[:-1]
    if changed[0]=="~":
        neg = True
        name = changed[1]
        changed = changed[3:]
    else:
        name = changed[0]
        changed = changed[2:]
    splited = changed.split(",")
    splited = splitedFix(splited)
    #print splited
    size = len(splited)

    count = 0
    skip = 0
    point = 0
    for el in splited:
        #print el, size, count
        if skip==1:
            skip=0
        elif size == 1 or count == 0:

            if el[0].islower()==True:
                if size != 1 and len(el) ==1 :

                    var.append(el[0])
                    maps[point] = "v"+str(len(var)-1)
                    point+=1
                    #print var
                elif size == 1 and len(el)==1:
                    #print el, size, count
                    var.append(el[0])
                    maps[point] = "v"+str(len(var)-1)
                    point+=1
                elif size==1:
                    #print el, size, count
                    temp = funcHandle(el[:-1])
                    func.append(temp)
                    maps[point] = "f"+str(len(func)-1)
                    point+=1
                else:
                    #print el, size, count
                    temp = funcHandle(el)
                    func.append(temp)
                    maps[point] = "f"+str(len(func)-1)
                    point+=1
            else:
                cons.append(el[0])
                maps[point] = "c"+str(len(cons)-1)
                point+=1
            count+=1



        elif count == size:
            #print el[0]
            if el[0].islower()==True:
                if len(el) == 2:
                    var.append(el[0])
                    maps[point] = "v"+str(len(var)-1)
                    point+=1
                else:
                    temp = funcHandle(el[0:-1])
                    func.append(temp)
                    maps[point] = "f"+str(len(func)-1)
                    point+=1
            else:
                cons.append(el[0])
                maps[point] = "c"+str(len(cons)-1)
                point+=1
            count+=1
        else:
            if el[0].islower()==True:
                if len(el) == 1:
                    var.append(el[0])
                    maps[point] = "v"+str(len(var)-1)
                    point+=1
                else:
                    temp = funcHandle(el[0:])
                    func.append(temp)
                    maps[point] = "f"+str(len(func)-1)
                    point+=1
            else:
                cons.append(el[0])
                maps[point] = "c"+str(len(cons)-1)
                point+=1
            count+=1
    #print var
    result = literal(name,var,func,cons,neg,maps)
    if b_g == 0:
        base[loc].append(result)
    else:
        goal[loc].append(result)


def unify(bas,go):
    global use
    global deriv
    global deriv_n
    maps = {}
    for i in go:
        for j in bas:
            if i.name ==j.name and i.neg !=j.neg:
                print i.name

def sub():
    global deriv
    global deriv_n
    global use

    for i in deriv:
        for j in i:
            key = j.name+str(not j.neg)
            if key in use:
                work = use[key]
                for k in work:
                    unify(k,i)
def resol():
    global deriv
    global deriv_n
    global use

    for i in goal:
        deriv.append(i)
        for j in i:
            deriv_n.append(j.name)
    for i in base:
        for j in i:
            if deriv_n.count(j.name)>0:
                key = j.name+str(j.neg)
                if key in use :
                    use[key].append(i)
                else:
                    use[key] = []
                    use[key].append(i)
    while len(use)>0:
        sub()


f = open("input.txt","r")
w = open("output.txt","w")
lines = f.readlines()
counter = 0;
cases = int(lines[counter].split("\n")[0])
counter+=1
for i in range(0,cases):
    deriv = []
    deriv_n = []
    use = {}
    spliter  = lines[counter].split("\n")[0]
    counter+=1
    spliter =  spliter.split(" ")
    bc = int(spliter[0])
    gc = int(spliter[1])
    base = []
    for k in range(0,bc):
        spliter = lines[counter].split("\n")[0]
        counter+=1
        neg = False
        var = []
        func = []
        cons = []
        nextname = 0
        base.append([])
        lc = -1
        changed = ""
        skip = 0
        #print spliter
        for j in spliter:
        #    print j
#            print changed,j,lc
            if skip==1:
                skip=0
            elif j=="(" and lc==-1 :
                lc=1
                changed+=j
            elif j=="(" and lc!=-1:
                lc+=1
                changed+=j
            elif j==")":
                lc-=1
                if(lc==0):
                    changed+=j
                    parser(changed,k,0)
                    changed = ""
                    lc = -1
                    skip=1
                else:
                    changed+=j

            else:
                changed+=j
    for k in range(0,gc):
        spliter = lines[counter].split("\n")[0]
        counter+=1
        neg = False
        var = []
        func = []
        cons = []
        nextname = 0
        goal.append([])
        lc = -1
        changed = ""
        skip = 0
        #print spliter
        for j in spliter:
        #    print j
#            print changed,j,lc
            if skip==1:
                skip=0
            elif j=="(" and lc==-1 :
                lc=1
                changed+=j
            elif j=="(" and lc!=-1:
                lc+=1
                changed+=j
            elif j==")":
                lc-=1
                if(lc==0):
                    changed+=j
                    parser(changed,k,1)
                    changed = ""
                    lc = -1
                    skip=1
                else:
                    changed+=j

            else:
                changed+=j
    result = resol()

for i in base:
    for j in i:
        pass
#        printLiteral(j)
