from tqdm import tqdm
from discource_parser import *

class Replica():

    def __init__(self, speaker):
        self.speaker = speaker
        self.content = []

    def add(self, unit):
        # выбрасывать ошибку, если не подряд
        if not isinstance(unit, Unit): raise TypeError('Only units in replicas!')
        self.content.append(unit)

    def get_time_length(self):
        return self.content[-1].time - self.content[0].time

    def str_w_time(self):
        length_str = str(self.get_time_length())
        return f'(len={length_str}) ' + str(self)

    def __repr__(self):
        return str(self.content)

    def __len__(self):
        return len(self.content)

    def __str__(self):
        return ' '.join(str(u) for u in self.content)

    def __bool__(self):
        return len(self) > 0
    
    @property
    def time(self):
        return self.content[0].time

#  можно добавить время с по
def get_replica_list(units_list, speaker, min_unit_amount = 2):
    res = []
    current_replica = Replica(speaker)
    for unit in tqdm(filter(lambda u: u.speaker == speaker, units_list)):
        if isinstance(unit, PauseUnit) and unit.is_boundary:
            if current_replica:
                if len(current_replica) >= min_unit_amount: res.append(current_replica)
                del current_replica
            current_replica = Replica(speaker)
        else:
            if not current_replica: current_replica = Replica(speaker)
            current_replica.add(unit)
    if len(current_replica) >= min_unit_amount: res.append(current_replica)
    return res