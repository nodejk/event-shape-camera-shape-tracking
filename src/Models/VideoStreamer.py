import cv2 as cv
from dv import NetworkFrameInput

class VideoStream:
    camera: cv.VideoCapture
    address: str
    port: int

    def __init__(self, address: str, port: int) -> None:
        self.address = address
        self.port = port

        # self.camera = cv.VideoCapture(url)

        # if not self.camera.isOpened():
        #     print('Camera not working')
        #     exit()
    
        pass

    def getStream(self):
        with NetworkFrameInput(address=self.address, port=self.port) as stream:
            for frame in stream:
                yield frame
        
        # while True:
        #     ret, frame = self.camera.read()
            
        #     if not ret:
        #         print("Can't receive frame (stream end?). Exiting ...")
        #         break
            
        #     gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        #     if cv.waitKey(1) == ord('q'):
        #         break

        #     yield frame.image
            