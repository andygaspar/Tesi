import numpy as np
import xpress as xp

xp.init()
m = xp.problem()

x = xp.var("x", xp.continuous)

y = xp.var(name="y", vartype=xp.continuous)
m.addVariable(x, y)
cons = x+y >= 5
m.addConstraint(cons)
obj = 2*x + 3*y
m.setObjective(obj, sense=xp.minimize)
m.solve()

print("status: ", m.getProbStatus())
print("string: ", m.getProbStatusString())

print("solution:", m.getSolution())

print("Attributes: ----------------------------------------")
print(m.getAttrib())

print("Controls: -------------------------------------------")
print(m.getControl())

help(xp)


print("ciao")