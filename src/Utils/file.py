import datetime
import hashlib


def random_file_name_generator() -> str:
    current_timestamp: str = datetime.datetime.now().isoformat()
    file_name: str = hashlib.sha1(str.encode(current_timestamp)).hexdigest()[0:10]

    return file_name
