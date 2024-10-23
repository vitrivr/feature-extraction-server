
from feature_extraction_server.core.model import Model
import logging
logger = logging.getLogger(__name__)

def is_cuda_available():
    if not torch.cuda.is_available():
        return False
    try:
        # Try to perform a simple CUDA operation
        torch.zeros(1).to('cuda')
        return True
    except Exception:
        return False

class DetrResnet101(Model):

    def _load_model(self):
        global torch
        import torch
        from transformers import DetrImageProcessor, DetrForObjectDetection
        self.processor = DetrImageProcessor.from_pretrained("facebook/detr-resnet-101")
        self.model = DetrForObjectDetection.from_pretrained("facebook/detr-resnet-101")
        
        self.model.eval()
        if is_cuda_available():
            if self.no_cuda:
                logger.debug("CUDA is available but not being used due to --no-cuda setting.")
                self.device = torch.device("cpu")
            else:
                logger.debug("CUDA is available and being used.")
                self.device = torch.device("cuda")
        else:
            logger.debug("CUDA is not available. Using CPU.")
            self.device = torch.device("cpu")
        self.model.to(self.device)

    def object_detection(self, image, config={}):
        image = image.to_numpy()
        inputs = self.processor(images=image, return_tensors="pt")
        
        with torch.no_grad():
            outputs = self.model(**inputs, **config)

        # convert outputs (bounding boxes and class logits) to COCO API
        # let's only keep detections with score > 0.9
        target_sizes = torch.tensor([image.size[::-1]])
        single_results = self.processor.post_process_object_detection(outputs, target_sizes=target_sizes, threshold=0.9)[0]
        return {
            "scores": single_results['scores'].tolist(), 
            "labels": [self.model.config.id2label[int(i)] for i in single_results['labels']], 
            "boxes": single_results['boxes'].tolist()
        }