import numpy as np
import time

start_time = time.time()

def pattern(level):
    global base_pattern
    global sequence
    current_id = 0
    first_burned = False
    items_to_return = len(sequence)
    while True:
        for _ in range(0, level):
            if not first_burned:
                first_burned = True
                continue
            yield base_pattern[current_id]
            items_to_return -= 1
            if items_to_return <= 0:
                return
        current_id = (current_id + 1) % len(base_pattern)

input = "59769638638635227792873839600619296161830243411826562620803755357641409702942441381982799297881659288888243793321154293102743325904757198668820213885307612900972273311499185929901117664387559657706110034992786489002400852438961738219627639830515185618184324995881914532256988843436511730932141380017180796681870256240757580454505096230610520430997536145341074585637105456401238209187118397046373589766408080120984817035699228422366952628344235542849850709181363703172334788744537357607446322903743644673800140770982283290068502972397970799328249132774293609700245065522290562319955768092155530250003587007804302344866598232236645453817273744027537630"
# input = '12345678'
# input = '80871224585914546619083218645595'

sequence = [int(ch) for ch in input]
patterns = []
base_pattern = [0, 1, 0, -1]

# build patterns matrix
for level in range(0, len(sequence)):
    next_level = [x for x in pattern(level+1)]
    patterns.append(next_level)

sequence = np.array(sequence)
patterns = np.array(patterns)

for _ in range(0, 100):
    # Using these native numpy functions is way faster than iterating through the sequence
    sequence = np.mod(np.abs(np.dot(patterns, sequence)), 10)

print(f'Time: {time.time() - start_time}')

print('First star answer:')
print(''.join(str(x) for x in sequence[0:8]))





