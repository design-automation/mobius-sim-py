import sys, os
import random
import time
sys.path.insert(0, os.path.abspath('..'))
from sim_model import sim
ENT_TYPE = sim.ENT_TYPE
DATA_TYPE = sim.DATA_TYPE

# start
t0 = time.time()

# position with random XYZ coords
def rand_posi():
    return sm.add_posi([random.random(), random.random(), random.random()])

# create a graph
sm = sim.SIM()

# coll
coll = sm.add_coll()

# create a points
for i in range(1000):
    point = sm.add_point(rand_posi())
    if random.random() > 0.1:
        sm.add_coll_ent(coll, point)

# create 1000 plines
for i in range(100):
    posis = []
    for j in range(random.randint(2, 30)):
        posis.append(rand_posi())
    pline = sm.add_pline(posis, True)
    if random.random() > 0.1:
        sm.add_coll_ent(coll, pline)

# create 1000 pgons
for i in range(1000):
    posis = []
    for j in range(random.randint(3, 30)):
        posis.append(rand_posi())
    pgon = sm.add_pgon(posis)
    if random.random() > 0.1:
        sm.add_coll_ent(coll, pgon)

# write to str
json = sm.to_json_str()
# with open("test.sim", "w") as f:
#     f.write(json)

# calc time
t1 = time.time()
print "Time = ", t1 - t0