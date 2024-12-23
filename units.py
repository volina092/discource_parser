from dataclasses import dataclass
from tqdm import tqdm

# Абстрактный класс для дискурсивной единицы
@dataclass
class Unit:
    speaker: str # id в тг
    time: int # unixType


class TextUnit(Unit):
    # атрибуты: speaker, time, text

    def __init__(self, speaker, time, text):
        super().__init__(speaker, int(time))
        # по идее такого случиться не может, но мало ли что...
        if not text: print(f'ALARM: TextUnit({self.speaker} at {self.time}) with empty text!') # можно ли сделать какой-то питоновый варнинг?
        self.text = text
        
    def __repr__(self):
        # в идеале тоже вынести в конфиг
        if len(self) < 30: return f'{self.speaker}: {self.text}'
        return f'{self.speaker}: {self.text[:30]}...'

    def __str__(self):
        return self.text.strip()

    def __len__(self):
        return len(self.text)


class MediaUnit(Unit):
    # атрибуты: speaker, time

    def __init__(self, speaker, time):
        super().__init__(speaker, int(time))

    def __repr__(self):
        return f'{self.speaker}: [media]'

    def __str__(self):
        return '[media]'


class PauseUnit(Unit):
    # атрибуты: speaker, time

    def __init__(self, speaker, time_starts, time_ends, max_pause_replica):
        super().__init__(speaker, int(time_starts))
        self.end_time = int(time_ends)
        self.is_boundary = len(self) > max_pause_replica # граница реплики или нет
        self.has_interruption = False

    def set_interruption(self, value: bool = True):
        self.has_interruption = value
    
    def __repr__(self):
        return f'{self.speaker}: ' + str(self)

    def __str__(self):
        i_marker = '!' if self.has_interruption else ''
        if len(self) <= 1: return f'({i_marker}≤1)'
        return f'({i_marker}{len(self)})'

    def __len__(self): # длина паузы в секундах
        return self.end_time - self.time
