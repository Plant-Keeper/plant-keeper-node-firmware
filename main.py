import gc
import random
from pk import PlantKeeper
import node_type

pk = PlantKeeper(host='10.3.141.1', port=8001)
pk.set_node_type(node_type=node_type.SPRINKLER)

if __name__ == '__main__':
    while True:
        sensor = random.randint(10, 30)
        pk.post({"soil_humidity": sensor, 'tag': 'orchid'})
        print(pk.power)
        gc.collect()
