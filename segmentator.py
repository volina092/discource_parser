import json
from tqdm import tqdm
from discource_parser import *

from discource_parser import configurator
DEFAULTS = configurator.config['DEFAULT']

class ChatSegmentator:

    def __init__(self, max_pause_replica = DEFAULTS['max_pause_replica'], max_pause_text = DEFAULTS['max_pause_text']):
        self.max_pause_replica = max_pause_replica
        self.max_pause_text = max_pause_text
        self.chat_segments = []

    
    def process_file(self, path):
        try: 
            with open(path, 'r', encoding='utf-8') as f:
                chat_dict = json.load(f)
            msg_list = chat_dict['messages']
        except:
            raise JSONDecodeError("Incorrect path or file is defective")
        
        speakers_pauses_started = dict()
        for i in tqdm(range(len(msg_list))):
            # делаем из стрёмного объекта прикольный юнит
            if msg_list[i]['type'] != 'message': continue
            # можно сделать спец класс "пересланное сообщение", но зачем?
            elif 'forwarded_from' in msg_list[i]:
                current_unit = self.get_media_unit_from_msg(msg_list[i])
            else: current_unit = self.get_unit_from_msg(msg_list[i])
            
            # добавляем паузу, если она нужна, засекаем начало следующей паузы
            if current_unit.speaker in speakers_pauses_started:
                self.chat_segments.append(PauseUnit(
                    current_unit.speaker,
                    speakers_pauses_started[current_unit.speaker],
                    current_unit.time,
                    self.max_pause_replica
                ))
            # запоминаем для будущей паузы
            speakers_pauses_started[current_unit.speaker] = current_unit.time
            self.chat_segments.append(current_unit)
            # сортируем ? хотя всё по порядку добавили
    
    def get_unit_from_msg(self, msg):
        adopted_msg = AdoptedTgMessage(msg)
        if adopted_msg.text:
            return TextUnit(adopted_msg.speaker, adopted_msg.time, adopted_msg.text)
        return MediaUnit(adopted_msg.speaker, adopted_msg.time)

    
    def get_media_unit_from_msg(self, msg):
        adopted_msg = AdoptedTgMessage(msg)
        return MediaUnit(adopted_msg.speaker, adopted_msg.time)
        
    def set_if_pauses_interrupted(self):
        # TMP проверить мб надо список
        non_boundary_pauses = filter(lambda u: isinstance(u, PauseUnit) and not u.is_boundary, self.chat_segments)
        for pause in non_boundary_pauses:
            # второй if можно отдельной ф-цией 
            if sum(1 for u in self.chat_segments if not isinstance(u, PauseUnit) and pause.time < u.time < pause.end_time):
                pause.set_interruption()
    
    def get_speakers_list(self):
        return set(map(lambda u: u.speaker, self.chat_segments))
    
    def get_units_list(self):
        return self.chat_segments
