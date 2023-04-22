import cv2
import os

if __name__ == "__main__":
    root_path = "/src/GSCEventMOD/Sessions/28f3ee4ca3/"
    image_folder = os.path.join(root_path, "model_output")
    video_name = os.path.join(root_path, "video.avi")

    images = [img for img in os.listdir(image_folder) if img.endswith(".jpg")]
    frame = cv2.imread(os.path.join(image_folder, images[0]))
    height, width, layers = frame.shape

    video = cv2.VideoWriter(video_name, 0, 1, (width, height))

    for image in images:
        video.write(cv2.imread(os.path.join(image_folder, image)))

    cv2.destroyAllWindows()
    video.release()
