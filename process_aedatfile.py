from src.Models.AedatFileReader import AedatFileReader
from datetime import datetime
import os
from src.Models.Visualizer import Visualizer
import pathlib
import time
import hashlib


def generate_random_file_name() -> None:
    current_timestamp: str = datetime.now().isoformat()
    hash_digest: str = hashlib.sha1(str.encode(current_timestamp)).hexdigest()[0:20]

    return os.path.join(pathlib.Path(__file__).parent, 'data', hash_digest)


if __name__ == '__main__':
    
    path = 'C:/Users/Krishna/event-camera/dvSave-2022_11_29_19_20_59.aedat4'
    # path = 'C:/Users/Krishna/Desktop/pProjects/event-shape-camera-shape-tracking/Cars_sequence.aedat4'


    reader: AedatFileReader = AedatFileReader(
        path=path,
        height=0,
        width=0,
    )

    count = 0
    start_time = time.time()

    for frame in reader:
        # print(frame)
        # Visualizer.visualize(frame.image, "tes")
        count += 1
    
    end_time = time.time()
    print(end_time - start_time)
    
    print(count)

    print(count / (end_time - start_time))
    # print(time.time() - start_time)
        # break
        # Visualizer.visualize(frame.image, 'test')


    pass