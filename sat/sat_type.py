from enum import Enum, auto


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
