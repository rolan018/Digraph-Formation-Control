from enum import Enum, auto
from abc import ABC, abstractmethod


# class syntax
class SatType(Enum):
    MAIN = auto()
    SECONDARY = auto()
    
    @staticmethod
    def from_str(label: str):
        if label in ("SECONDARY", "SatType.SECONDARY"):
            return SatType.SECONDARY
        elif label in ("MAIN", "SatType.MAIN"):
            return SatType.MAIN
        else:
            raise NotImplementedError
        

# class syntax
class SatTypeRaft(Enum):
    CANDIDATE = auto()
    LEADER = auto()
    FOLLOWER = auto()
    CRASHED = auto()

    @staticmethod
    def from_str(label: str):
        if label in ("CANDIDATE", "SatTypeRaft.CANDIDATE"):
            return SatTypeRaft.CANDIDATE
        elif label in ("LEADER", "SatTypeRaft.LEADER"):
            return SatTypeRaft.LEADER
        elif label in ("FOLLOWER", "SatTypeRaft.FOLLOWER"):
            return SatTypeRaft.FOLLOWER
        elif label in ("CRASHED", "SatTypeRaft.CRASHED"):
            return SatTypeRaft.CRASHED
        else:
            raise NotImplementedError
