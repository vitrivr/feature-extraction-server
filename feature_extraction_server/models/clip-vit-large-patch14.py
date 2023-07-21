
from PIL import Image
import requests

from transformers import CLIPModel
from transformers import AutoTokenizer, CLIPTextModel, AutoProcessor, CLIPVisionModel

model = CLIPModel.from_pretrained("openai/clip-vit-large-patch14")

visionmodel = CLIPVisionModel.from_pretrained("openai/clip-vit-base-patch32")
processor = AutoProcessor.from_pretrained("openai/clip-vit-base-patch32")

textmodel = CLIPTextModel.from_pretrained("openai/clip-vit-base-patch32")
tokenizer = AutoTokenizer.from_pretrained("openai/clip-vit-base-patch32")





def text_embedding(text, config={}):
    inputs = tokenizer(text, padding=True, return_tensors="pt")

    outputs = textmodel(**inputs, **config)
    return outputs.pooler_output.tolist()

def image_embedding(image, config={}):
    inputs = processor(images=image, return_tensors="pt")

    outputs = visionmodel(**inputs, **config)
    return outputs.pooler_output.tolist()


def zero_shot_image_classification(image, classes, config):
    inputs = processor(text=classes, images=image, return_tensors="pt", padding=True)
    outputs = model(**inputs)
    logits_per_image = outputs.logits_per_image # this is the image-text similarity score
    probs = logits_per_image.softmax(dim=1) # we can take the softmax to get the label probabilities
    return probs.tolist()