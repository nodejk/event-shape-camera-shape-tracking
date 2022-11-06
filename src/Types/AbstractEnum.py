class AbstractEnum():
    def getAllValues(self,):
        classDictionary = self.__class__.__dict__
        return [classDictionary[i] for i in self.__class__.__dict__.keys() if i[:1] != '_']
