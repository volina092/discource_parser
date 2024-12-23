class AdoptedTgMessage: # адаптер тг-шных сообщений (к чему-то удобному нам)

    def __init__(self, msg_dict):
        self.msg_dict = msg_dict

    # @property
    # def is_text_message(self): return self.msg_dict['type'] == 'message'
    
    @property
    def time(self): return self.msg_dict['date_unixtime']
    
    @property
    def speaker(self):
        return self.msg_dict['from_id']

    @property
    def text(self):
        cleared_txt_ents = list(filter(lambda elem: elem['type'] != 'custom_emoji', self.msg_dict['text_entities']))
        joined_text = ''.join(map(lambda elem: elem['text'], cleared_txt_ents))
        if joined_text: return joined_text