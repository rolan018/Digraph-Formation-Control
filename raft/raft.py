from sat import Sat, SatTypeRaft
from .topology import FormationTopology
from graph.raft import RaftGraph

"""
Рафт протокол
"""
class ConsensusFormationControl():
    def __init__(self, sats: list[Sat]):
        self.topology = FormationTopology(sats)
        # Init process
        self.topology._startup_event()

    def process(self):
        self.topology.tick()
        for i, sat in enumerate(self.topology.sats):
            if sat.ticker == sat.ticker_timeout and sat.sat_type != SatTypeRaft.CRASHED:
                self.topology.leader_election(i)
                break
            if sat.sat_type == SatTypeRaft.CRASHED:
                self.crash_sat(i)
        self.topology.leader_heartbeat()

    def get_graph(self, with_waights: bool) -> RaftGraph:
        return RaftGraph(sat_matrix=[sat for sat in self.topology.sats], with_waights=with_waights)

    def crash_sat(self, sat_index):
        self.topology.sats[sat_index].sat_type = SatTypeRaft.CRASHED
        self.topology.crashed_indexes.append(sat_index)
    
    def crash_leader(self):
        self.crash_sat(self.get_leader_index())
    
    def add_sat_from_last_crashed(self):
        self.add_sat_from_crashed(self.topology.crashed_indexes[-1])

    def add_sat_from_crashed(self, sat_index):
        self.topology.crashed_indexes.remove(sat_index)
        self.topology.startup_event_for_sat(self.topology.sats[sat_index])

    def new_sat(self, sat: Sat):
        self.topology.startup_event_for_sat(sat)
    
    def get_leader_index(self):
        return self.topology.get_leader_index()
