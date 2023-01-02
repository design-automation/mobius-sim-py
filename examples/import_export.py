import sys, os
sys.path.insert(0, os.path.abspath('..'))
from sim_model import sim
from sim_model import io_sim
ENT_TYPE = sim.ENT_TYPE
DATA_TYPE = sim.DATA_TYPE

# create a graph
sm = sim.SIM()

io_sim.import_sim_file(sm, "pgon_hole.sim")
io_sim.export_sim_file(sm, "pgon_hole2.sim")