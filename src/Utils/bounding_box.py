import numpy
import typing


def non_max_suppression(bounding_boxes: numpy.ndarray, threshold: int = 0.1) -> numpy.ndarray:
    order = [1 for i in range(len(bounding_boxes))]
    keep = []


    while order:
        i = order.pop(0)
        keep.append(i)

        for j in order:
            # Calculate the IoU between the two boxes
            intersection = max(0, min(bounding_boxes[i][2], bounding_boxes[j][2]) - max(bounding_boxes[i][0], bounding_boxes[j][0])) * \
                           max(0, min(bounding_boxes[i][3], bounding_boxes[j][3]) - max(bounding_boxes[i][1], bounding_boxes[j][1]))
            union = (bounding_boxes[i][2] - bounding_boxes[i][0]) * (bounding_boxes[i][3] - bounding_boxes[i][1]) + \
                    (bounding_boxes[j][2] - bounding_boxes[j][0]) * (bounding_boxes[j][3] - bounding_boxes[j][1]) - intersection
            iou = intersection / union

            # Remove boxes with IoU greater than the threshold
            if iou > threshold:
                order.remove(j)

    print('keep-->', keep)
    return keep