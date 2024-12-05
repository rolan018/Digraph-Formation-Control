import numpy as np
from sat import Sat, SatTypeRaft

"""
Получаем 
"""
class ConsensusFormationControl():
    def __init__(self, sats: list[Sat]):
        self.sats = sats
        self.leader_index = None
        self.number_of_nodes = len(sats)
    
    def receipt_event(self, event):
        self.event = event
        # Special event starts leader election
        self.leader_election()
        # 

    def receipt_new_node(self):


    def leader_election(self):
        if self.leader_index is None:
            # Sync step
            for i, sat in enumerate(self.sats):
                sat.relative_distance = ConsensusFormationControl.relative_distance(i, self.sats)
            # 
            

    def startup_event(self):
        for sat in self.sats:
            sat.sat_type = SatTypeRaft.FOLLOWER
    
    @staticmethod    
    def relative_distance(index: int, sats: list[Sat]):
        result_distance = 0
        for i in range(len(sats)):
            if index != i:
                osk_i = sats[i].get_position(-1, "osk")
                osk_j = sats[index].get_position(-1, "osk")
                distance = np.round(np.linalg.norm(osk_i-osk_j), 2)
                result_distance += distance
        return result_distance
    
    def election(self, election_state):
        for sat in self.sats:



    
    def step(self):
       pass 