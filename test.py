from sim_model import sim
ENT_TYPE = sim.ENT_TYPE
DATA_TYPE = sim.DATA_TYPE

# create a graph
sm = sim.SIM()
# create posi
posi = sm.add_posi([1,2,3])
# create a point
point = sm.add_point(posi)
# create a pline
pline = sm.add_pline(
    [posi, sm.add_posi([4,5,7]), sm.add_posi([2,2,2])],
    True
)
# create  pgon
pgon = sm.add_pgon(
    [posi, sm.add_posi([2,3,4]), sm.add_posi([8,5,0])]
)
# create an coll
coll = sm.add_coll()
sm.add_coll_ent(coll, point)
sm.add_coll_ent(coll, pline)
sm.add_coll_ent(coll, pgon)

# create attributes
sm.add_attrib(ENT_TYPE.COLLS, "aaa", DATA_TYPE.LIST)
sm.add_attrib(ENT_TYPE.PGONS, "bbb", DATA_TYPE.NUM)

# set entity attrib value
sm.set_attrib_val(coll, "aaa", [1,2,3,4,5,6])
sm.set_attrib_val(pgon, "bbb", 1.2345)

# get the attribute value
val1 = sm.get_attrib_val(coll, "aaa")
val2 = sm.get_attrib_val(pgon, "bbb")

# set model attribute values
sm.set_model_attrib_val("ccc", "This is a test")
val3 = sm.get_model_attrib_val("ccc")

# ptint attrib vals
print("Attrib values:", val1, val2, val3)

# print info about the graph
print(sm.info())
print(sm.json_str())