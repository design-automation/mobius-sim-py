import sys, os
sys.path.insert(0, os.path.abspath('..'))
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
    True # closed
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
