import numpy as np
import random
from sat import Sat, SatTypeRaft

"""
Класс обслуживает топологию взаимодействия агентов 
"""
class FormationTopology():
    def __init__(self, sats: list[Sat]):
        self.sats = sats
        self.crashed_indexes: list[int] = []
        self._leader_index = None
        self.number_of_nodes = len(sats)
        self._max_epoch = 0
    
    def get_leader_index(self) -> int:
        return self._leader_index

    def tick(self):
        for sat in self.sats:
            if sat.sat_type != SatTypeRaft.LEADER and sat.sat_type != SatTypeRaft.CRASHED:
                sat.ticker += 1

    def startup_event_for_sat(self, sat: Sat):
        self._update_ticker(sat)
        sat.epoch = 0
        sat.sat_type = SatTypeRaft.FOLLOWER

    def leader_heartbeat(self):
        self._leader_index = self._validate_leader()
        if self._leader_index != None:
            for sat in self.sats:
                self._update_ticker(sat)
        self._validate_epoch()
    
    def leader_election(self, sat_index):        
        self.sats[sat_index].sat_type = SatTypeRaft.CANDIDATE
        # Sync step
        relative_distance = []
        for i in range(len(self.sats)):
            if self.sats[i].sat_type != SatTypeRaft.CRASHED:
                relative_distance.append((i, FormationTopology.relative_distance(i, self.crashed_indexes, self.sats)))
        # modelling election with min relative distance
        relative_distance.sort(key = lambda item: item[1])
        if relative_distance[0][0] == sat_index:
            self.sats[sat_index].sat_type = SatTypeRaft.LEADER
            self._leader_index = sat_index
        else:
            self.sats[sat_index].sat_type = SatTypeRaft.FOLLOWER
            self.sats[relative_distance[0][0]].sat_type = SatTypeRaft.LEADER
            self._leader_index = relative_distance[0][0]
        self.new_epoch()

    def new_epoch(self):
        for sat in self.sats:
            sat.epoch += 1
        self._max_epoch += 1

    def _validate_epoch(self):
        for sat in self.sats:
            if sat.epoch < self._max_epoch:
                # Добавляем записи в журнал отстающих агентов
                sat.epoch = self._max_epoch

    def _validate_leader(self) -> int:
        # Лидер всегда 1, с максимальной эпохой
        leader_indexes = []
        for i, sat in enumerate(self.sats):
            if sat.sat_type == SatTypeRaft.LEADER:
                leader_indexes.append((i, sat.epoch))
        if len(leader_indexes) == 0:
            return None
        leader_indexes.sort(key = lambda item: item[1], reverse=True)
        for leader in leader_indexes[1:]:
            self.sats[leader[0]].sat_type == SatTypeRaft.FOLLOWER
        return leader_indexes[0][0]
    
    def _startup_event(self):
        for sat in self.sats:
            self._update_ticker(sat)
            sat.epoch = 0
            sat.sat_type = SatTypeRaft.FOLLOWER
    
    def _update_ticker(self, sat: Sat):
        sat.ticker = 0
        sat.ticker_timeout = random.randint(3, 5)

    @staticmethod
    def relative_distance(index: int, crashed_indexes: list[int], sats: list[Sat]):
        result_distance = 0
        for i in range(len(sats)):
            if index != i and i not in crashed_indexes:
                osk_i = sats[i].get_position(-1, "osk")
                osk_j = sats[index].get_position(-1, "osk")
                distance = np.round(np.linalg.norm(osk_i-osk_j), 2)
                result_distance += distance
        return result_distance