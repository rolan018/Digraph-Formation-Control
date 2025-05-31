import numpy as np
import random
from sat import Sat, SatTypeRaft

"""
Класс обслуживает топологию взаимодействия агентов 
"""

TICKER_TIMEOUT_MIN = 100
TICKER_TIMEOUT_MAX = 150
STARTUP_TICKER_TIMEOUT_MIN = 3
STARTUP_TICKER_TIMEOUT_MAX = 5


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
        index_list = [i for i in range(len(self.sats))]
        for i in range(len(self.sats)):
            if self.sats[i].sat_type != SatTypeRaft.CRASHED:
                relative_distance.append((i, self._relative_distance(i, index_list)))
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
            self._startup_update_ticker(sat)
            sat.epoch = 0
            sat.sat_type = SatTypeRaft.FOLLOWER
    
    def _update_ticker(self, sat: Sat):
        sat.ticker = 0
        sat.ticker_timeout = random.randint(TICKER_TIMEOUT_MIN, TICKER_TIMEOUT_MAX)
    
    def _startup_update_ticker(self, sat: Sat):
        sat.ticker = 0
        sat.ticker_timeout = random.randint(STARTUP_TICKER_TIMEOUT_MIN, STARTUP_TICKER_TIMEOUT_MAX)

    def _relative_distance(self, index: int, index_list: list[int]):
        osk_i = self.sats[index].get_position(-1, "osk")
        result_distance = 0
        for j, sat in enumerate(self.sats):
            if index != j and j not in self.crashed_indexes and j in index_list:
                osk_j = sat.get_position(-1, "osk")
                distance = np.round(np.linalg.norm(osk_i-osk_j), 2)
                result_distance += distance
        return result_distance
    
    def _relative_vision(self, target_index) -> list[int]:
        vision_list: list[int] = 0
        osk_target = self.sats[target_index].get_position(-1, "osk")
        for i, sat in enumerate(self.sats):
            if i != target_index:
                osk_i = sat.get_position(-1, "osk")
                distance = np.round(np.linalg.norm(osk_target-osk_i), 2)
                if distance <= self.sats[target_index].vision_param:
                    vision_list.append(i)
        return vision_list

    def _phi_parametr(self, index: int):
        # считаем кол-во видимых спутников
        alpha = self._relative_vision(index)
        # считаем расстояние до видимых спутников
        betta = self._relative_distance(index, alpha)
        return len(alpha) + 1/betta
