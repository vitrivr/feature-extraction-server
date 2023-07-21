from transformers import DetrImageProcessor, DetrForObjectDetection
import torch
from PIL import Image
import requests

url = "http://images.cocodataset.org/val2017/000000039769.jpg"
image = Image.open(requests.get(url, stream=True).raw)

processor = DetrImageProcessor.from_pretrained("facebook/detr-resnet-101")
model = DetrForObjectDetection.from_pretrained("facebook/detr-resnet-101")


def object_detection(image, config={}):
    results = []
    for single_image in image:
        inputs = processor(images=single_image, return_tensors="pt")
        outputs = model(**inputs, **config)

        # convert outputs (bounding boxes and class logits) to COCO API
        # let's only keep detections with score > 0.9
        target_sizes = torch.tensor([single_image.size[::-1]])
        single_results = processor.post_process_object_detection(outputs, target_sizes=target_sizes, threshold=0.9)[0]
        
        single_results = {
            'scores': single_results['scores'].tolist(),
            'labels': [model.config.id2label[int(i)] for i in single_results['labels']],
            'boxes': single_results['boxes'].tolist(),
        }
        results.append(single_results)
    
    return results