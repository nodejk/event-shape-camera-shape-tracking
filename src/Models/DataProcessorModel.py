from abc import abstractmethod

class DataProcessorModel():
    @abstractmethod
    def inputFile(self, filePath):
        pass

    @abstractmethod
    def processData(self):
        pass
