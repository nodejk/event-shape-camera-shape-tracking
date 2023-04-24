import argparse
import typing

import cv2
import os
import glob


def image_file_sort(s: str) -> int:
    return int(os.path.basename(s)[:-4])


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--session_path", help="path of configuration")
    args = parser.parse_args()

    output_dir: str = os.path.join(args.session_path, "model_output")

    images: typing.List[str] = glob.glob(output_dir + "/*.jpg")

    images.sort(key=image_file_sort)

    video_name: str = "video.avi"

    frame = cv2.imread(images[0])
    height, width, layers = frame.shape

    video = cv2.VideoWriter(video_name, 0, 30, (width, height))

    for image in images:
        video.write(cv2.imread(image))

    cv2.destroyAllWindows()
    video.release()
