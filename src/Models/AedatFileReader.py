from dv import AedatFile

class AedatFileReader:
    path: str
    height: int
    width: int

    def __init__(self, path: str) -> None:
        self.path = path

        with AedatFile(self.path) as aedat_file:
            self.height, self.width = aedat_file['events'].size
    
    def __next__(self):
        with AedatFile(self.path) as aedat_file:
            print(aedat_file.names)

            for frame in aedat_file['frames']:
                yield frame.image
    
    def dimensions(self):
        return [self.height, self.width]
