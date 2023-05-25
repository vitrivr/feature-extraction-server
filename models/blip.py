import utils
from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration

processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

defaults = {}

def batch(iterable, n=1):
    l = len(iterable)
    for ndx in range(0, l, n):
        yield iterable[ndx:min(ndx + n, l)]


def caption(image, inference_args={}):
    # Set defaults if not provided
    args = defaults.copy()
    args.update(inference_args)
    
    inputs = processor(image, return_tensors="pt")

    output_ids = model.generate(**inputs, **inference_args)
    preds = processor.batch_decode(output_ids, skip_special_tokens=True)
    preds = [pred.strip() for pred in preds]
    return list(batch(preds, len(preds)//len(image)))

def conditional_caption(image, text, inference_args={}):
    # Set defaults if not provided
    args = defaults.copy()
    args.update(inference_args)
    
    inputs = processor(image, text=[text]*len(image), return_tensors="pt")

    output_ids = model.generate(**inputs,  **inference_args)
    preds = processor.batch_decode(output_ids, skip_special_tokens=True)
    preds = [pred.strip() for pred in preds]
    return list(batch(preds, len(preds)//len(image)))