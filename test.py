from sim_model import sim
ENT = sim.ENT
TYPE = sim.TYPE

# create a graph
sm = sim.SIM()
# create posi
posi = sm.addPosi([1,2,3])
# create a point
point = sm.addPoint(posi)
# create a pline
pline = sm.addPline(
    [posi, sm.addPosi([4,5,7]), sm.addPosi([2,2,2])],
    True
)
# create  pgon
pgon = sm.addPgon(
    [posi, sm.addPosi([2,3,4]), sm.addPosi([8,5,0])]
)
# create an coll
coll = sm.addColl()
sm.addCollEnt(coll, point)
sm.addCollEnt(coll, pline)
sm.addCollEnt(coll, pgon)

# create attributes
attrib_a = sm.addAttrib(ENT.COLLS, "aaa", TYPE.LIST)
attrib_b = sm.addAttrib(ENT.PGONS, "bbb", TYPE.NUM)

# set entity attrib value
sm.setEntAttribVal(coll, attrib_a, [1,2,3,4,5,6])
sm.setEntAttribVal(pgon, attrib_b, 1.2345)

# get the attribute value
val1 = sm.getEntAttribVal(coll, attrib_a)
val2 = sm.getEntAttribVal(pgon, attrib_b)

# set model attribute values
sm.setModelAttribVal("ccc", "This is a test")
val3 = sm.getModelAttribVal("ccc")

# ptint attrib vals
print("Attrib values:", val1, val2, val3)

# print info about the graph
print(sm.info())
