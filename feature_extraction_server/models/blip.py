import utils
from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration
import torch
from utils import batch

processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

defaults = {}




def image_captioning(image, config={}):
    # Set defaults if not provided
    args = defaults.copy()
    args.update(config)
    
    inputs = processor(image, return_tensors="pt")
    inputs = {k: v.to(model.device) for k, v in inputs.items()}
    with torch.no_grad():
        output_ids = model.generate(**inputs, **config)
    preds = processor.batch_decode(output_ids, skip_special_tokens=True)
    preds = [pred.strip() for pred in preds]
    return list(batch(preds, len(preds)//len(image)))

def conditional_image_captioning(image, text, config={}):
    # Set defaults if not provided
    args = defaults.copy()
    args.update(config)
    
    inputs = processor(image, text=[text]*len(image), return_tensors="pt")
    inputs = {k: v.to(model.device) for k, v in inputs.items()}
    with torch.no_grad():
        output_ids = model.generate(**inputs,  **args)
    preds = processor.batch_decode(output_ids, skip_special_tokens=True)
    preds = [pred.strip() for pred in preds]
    return list(batch(preds, len(preds)//len(image)))