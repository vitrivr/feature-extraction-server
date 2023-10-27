installation_command = "pip install transformers torch"


def load_model():
    global model, processor, tokenizer
    from transformers import CLIPModel
    from transformers import AutoTokenizer, AutoProcessor

    model = CLIPModel.from_pretrained("openai/clip-vit-large-patch14")
    processor = AutoProcessor.from_pretrained("openai/clip-vit-large-patch14")
    tokenizer = AutoTokenizer.from_pretrained("openai/clip-vit-large-patch14")


def text_embedding(text, config={}):
    inputs = tokenizer(text, padding=True, return_tensors="pt")

    outputs = model.get_text_features(**inputs, **config)
    return outputs.tolist()

def image_embedding(image, config={}):
    inputs = processor(images=list(map(lambda x: x.to_numpy(), image)), return_tensors="pt")

    outputs = model.get_image_features(**inputs, **config)
    return outputs.tolist()


def zero_shot_image_classification(image, classes, config={}):
    inputs = processor(text=classes, images=list(map(lambda x: x.to_numpy(), image)), return_tensors="pt", padding=True)
    outputs = model(**inputs)
    logits_per_image = outputs.logits_per_image # this is the image-text similarity score
    probs = logits_per_image.softmax(dim=1) # we can take the softmax to get the label probabilities
    return probs.tolist()