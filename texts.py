from tqdm import tqdm
import os.path
from itertools import groupby
from discource_parser import *

class Text():

    def __init__(self, replicas: list = []):
        # выбрасывать ошибку если в листе не реплики
        self.replicas = replicas

    def add(self, replicas: Replica):
        self.replicas.append(unit)

    def add_from_list(self, r_list: list):
        self.replicas += r_list

    def sort_replicas(self):
        # выбрасывать ошибку если в листе не реплики
        replicas = [r for r, _ in groupby(self.replicas)]
        self.replicas = sorted(replicas, key = lambda r: r.time)

    def __repr__(self):
        return str(self.replicas)
    
    def __str__(self):
        res = ''
        for replica in self.replicas:
            res += f'{replica.speaker} ({replica.get_time_length()}):\n{str(replica)}\n\n'
        return res
    
    def save_to_txt(self, path):
        # проверить, что путь ок
        if not path.endswith('.txt'): raise TypeError('Output file is suppised to be .txt')
        elif os.path.exists(path): raise NameError('File with this path already exists')
        with open(path, 'w', encoding='utf-8') as f:
            f.write(str(self))
            