import torch
from PIL import Image
import requests
from transformers import Blip2Processor, Blip2ForConditionalGeneration
from utils import batch

defaults = {}

device = "cuda" if torch.cuda.is_available() else "cpu"

processor = Blip2Processor.from_pretrained("Salesforce/blip2-opt-2.7b")
model = Blip2ForConditionalGeneration.from_pretrained(
    "Salesforce/blip2-opt-2.7b", torch_dtype=torch.float
)
model.to(device)



def conditional_caption(image, text, inference_args={}):
    # Set defaults if not provided
    args = defaults.copy()
    args.update(inference_args)
    
    inputs = processor(images=image, text=[text]*len(image), return_tensors="pt")
    inputs = {k: v.to(model.device) for k, v in inputs.items()}
    with torch.no_grad():
        output_ids = model.generate(**inputs,  **args)
    preds = processor.batch_decode(output_ids, skip_special_tokens=True)
    preds = [pred.strip() for pred in preds]
    return list(batch(preds, len(preds)//len(image)))