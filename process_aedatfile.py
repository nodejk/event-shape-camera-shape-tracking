from src.Models.FrameReaders.AedatFileFrameReader import AedatFileFrameReader
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
    
    # path = 'C:/Users/Krishna/event-camera/dvSave-2022_11_29_19_20_59.aedat4'
    path = "C:/Users/Krishna/event-camera/dvSave-2022_11_29_19_14_39.aedat4"
    # path: str = 'C:/Users/Krishna/Downloads/Raw_AEDAT4_Files/Cars_sequence.aedat4'

    reader: AedatFileFrameReader = AedatFileFrameReader(
        path=path,
    )

    count = 0
    start_time = time.time()

    for frame in reader:
        Visualizer.visualize(frame, "tes")
        count += 1
    
    end_time = time.time()
    print(end_time - start_time)
    
    print(count)

    print(count / (end_time - start_time))

