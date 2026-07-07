# Object Detection Metrics

## Precision
Precision measures how many detections made by the model were correct.

`Precision = True Positives / (True Positives + False Positives)`

High precision means fewer false alerts.

## Recall
Recall measures how many actual animals were detected by the model.

`Recall = True Positives / (True Positives + False Negatives)`

High recall means fewer missed animals.

## mAP@0.5
Mean Average Precision at IoU 0.5 measures how well the model detects objects when the predicted box overlaps the real box by at least 50%.

## mAP@0.5:0.95
This is a stricter metric that averages mAP across IoU thresholds from 0.5 to 0.95. It gives a more realistic view of bounding box quality.

## IoU
Intersection over Union measures overlap between the predicted bounding box and the ground truth bounding box.
