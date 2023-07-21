


import torch
from PIL import Image
from transformers import VisionEncoderDecoderModel, ViTImageProcessor, AutoTokenizer
from utils import batch

# Load the model, tokenizer and feature extractor outside the endpoint
model = VisionEncoderDecoderModel.from_pretrained("nlpconnect/vit-gpt2-image-captioning")
feature_extractor = ViTImageProcessor.from_pretrained("nlpconnect/vit-gpt2-image-captioning")
tokenizer = AutoTokenizer.from_pretrained("nlpconnect/vit-gpt2-image-captioning")

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

# Default values for max_length and num_beams
defaults = {}  #for more info on these args (and additional args), see https://huggingface.co/docs/transformers/main_classes/text_generation


def image_captioning(image, config={}):
    pixel_values = feature_extractor(images=image, return_tensors="pt").pixel_values
    pixel_values = pixel_values.to(device)

    # Set defaults if not provided
    args = defaults.copy()
    args.update(config)
    with torch.no_grad():
        output_ids = model.generate(pixel_values, **args)
    preds = tokenizer.batch_decode(output_ids, skip_special_tokens=True)
    preds = [pred.strip() for pred in preds]
    return list(batch(preds, len(preds)//len(image)))