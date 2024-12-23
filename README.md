Something like 

```
from discource_parser import *
segmentator = ChatSegmentator()


segmentator.process_file('my_best_friend/result.json')
segmentator.set_if_pauses_interrupted()
res = segmentator.get_units_list()

print(segmentator.get_speakers_list())

txt = Text(get_replica_list(res, 'user419896689', min_unit_amount=1))
txt.add_from_list(get_replica_list(res, 'user618290969', min_unit_amount=1))
txt.sort_replicas()

txt.save_to_txt('result_file.txt')
```
