from src.Models.AedatFileReader import AedatFileReader
from datetime import datetime
import os
import pathlib
import hashlib


def generate_random_file_name() -> None:
    current_timestamp: str = datetime.now().isoformat()
    hash_digest: str = hashlib.sha1(str.encode(current_timestamp)).hexdigest()[0:20]

    return os.path.join(pathlib.Path(__file__).parent, 'data', hash_digest)


if __name__ == '__main__':

    reader: AedatFileReader = AedatFileReader(
        path='C:/Users/Krishna/event-camera/dvSave-2022_11_29_19_20_59.aedat4'
    )

    for frame in reader:
        pass


    pass