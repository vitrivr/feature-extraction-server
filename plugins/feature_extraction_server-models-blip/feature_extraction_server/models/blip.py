

def load_model():
    global model, processor, defaults, torch, batch 
    
    from transformers import BlipProcessor, BlipForConditionalGeneration
    import torch
    from feature_extraction_server.core.utils import batch

    processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
    model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

    defaults = {}
    processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
    model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")


def image_captioning(image, config={}):
    # Set defaults if not provided
    args = defaults.copy()
    args.update(config)
    inputs = processor(list(map(lambda x: x.to_numpy(), image)), return_tensors="pt")
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
    
    inputs = processor(list(map(lambda x: x.to_numpy(), image)), text=text, return_tensors="pt", padding=True)
    inputs = {k: v.to(model.device) for k, v in inputs.items()}
    with torch.no_grad():
        output_ids = model.generate(**inputs,  **args)
    preds = processor.batch_decode(output_ids, skip_special_tokens=True)
    preds = [pred.strip() for pred in preds]
    return list(batch(preds, len(preds)//len(image)))