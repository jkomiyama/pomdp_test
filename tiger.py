class Node:
  def __init__(self, val, children):
    self.children = children
    self.val = val

def printTree(root, depth=0):
  print " "*depth,root.val
  if len(root.children)>0:
    for child in root.children:
      printTree(child, depth+1)

#Listen0 = Node((-1,-1), [])
#Left0 = Node((10,-100), [])
#Right0 = Node((-100,10), [])
#Theta0 = Node("0", [Listen0, Left0, Right0])
Theta0 = Node("Theta0", [])

def nextTheta(prevTheta, name):
  observationNum = 3
  children = []
  for o in range(observationNum):
    children.append(prevTheta)
  t = Node(name, children)
  return t

#action: [ActionListen, ActionOpenLeft, ActionOpenRight]
ActionListen, ActionOpenLeft, ActionOpenRight = 0, 1, 2
#observation: [ObsLeft, ObsRight, ObsUnif]
ObsLeft, ObsRight, ObsUnif = 0, 1, 2
#state : [StateLeft, StateRight]
StateLeft, StateRight = 0, 1
def PsTiger(sprime, s, a): #Pr(sprime| s, a)
  if not s in [0,1]:
    print "s must be in [0,1]";sys.exit()
  if not a in [0,1,2]:
    print "a must be in [0,1,2]";sys.exit()
  if not sprime in [0,1]:
    print "sprime must be in [0,1]";sys.exit()
  if a == ActionListen: #listen
    if s != sprime:
      return 0
    else:
      return 1
  if a == ActionOpenLeft:
    return 0.5
  if a == ActionOpenRight:
    return 0.5

def PoTiger(o, s, a): #Pr(o| s, a)
  if not s in [0,1]:
    print "s must be in [0,1]";sys.exit()
  if not a in [0,1,2]:
    print "a must be in [0,1,2]";sys.exit()
  if not o in [0,1,2]:
    print "o must be in [0,1,2]";sys.exit()
  if a == ActionListen: #listen
    if o == ObsUnif:
      return 0
    else:
      if o == ObsLeft and s == StateLeft:
        return 0.85
      if o == ObsRight and s == StateRight:
        return 0.85
      else:
        return 0.15
  if a == ActionOpenLeft:
    if o == ObsUnif:
      return 1
    else:
      return 0
  if a == ActionOpenRight:
    if o == ObsUnif:
      return 1
    else:
      return 0

def ip(b, theta): #inner product
  if len(b) != len(theta):
    print "two array length do not match";sys.exit()
  return sum([b[i]*theta[i] for i in range(len(b))])

beta = 0.95

#b: 2d vector tree: tree value function
def calcValue(b, tree):
  value = -10000
  if tree.val != "Theta0":
    for a in [ActionListen, ActionOpenLeft, ActionOpenRight]:
      valuetemp = ip(b, [(-1,-1),(10,-100),(-100,10)][a])
      for obs in [ObsLeft, ObsRight, ObsUnif]:
        obsProb = sum([b[s] * PoTiger(obs, s, a) for s in [0,1]])
        if obsProb != 0:
          bprime = [PoTiger(obs, s, a)*b[s]/obsProb for s in [0,1]]
          if a != ActionListen:
            bprime = (0.5, 0.5)
          #print "obs=",obs
          #print "bprime=",bprime
          #print "cv =",calcValue(bprime, tree.children[obs]) 
          valuetemp += beta * obsProb * calcValue(bprime, tree.children[obs])
      value = max(value, valuetemp)
    print a,tree.val, valuetemp
    #printTree(tree)
    return value
  else: #leaf
    value = -10000
    for a in [ActionListen, ActionOpenLeft, ActionOpenRight]:
      valuetemp = ip(b, [(-1,-1),(10,-100),(-100,10)][a])
      value = max(value, valuetemp)
    #print "leafvalue=",value
    return value
if True:
  #printTree(Theta0)
  #tree = Theta0
  #tree = nextTheta(Theta0, "Theta1")
  #tree = nextTheta(nextTheta(Theta0, "Theta1"), "Theta2")
  tree = nextTheta(nextTheta(nextTheta(Theta0, "Theta1"), "Theta2"), "Theta3")
  printTree(tree)
  #b = (0.5, 0.5)
  b = (1.0, 0.0)
  value = calcValue(b, tree)
  print "value("+str(b)+")="+str(value)
