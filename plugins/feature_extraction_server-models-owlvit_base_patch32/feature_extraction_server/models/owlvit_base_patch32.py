installation_command = "pip install transformers torch"

def load_model():
    global detector
    from transformers import pipeline

    checkpoint = "google/owlvit-base-patch32"
    detector = pipeline(model=checkpoint, task="zero-shot-object-detection")

def zero_shot_object_detection(image, classes, config={}):
    return detector(list(map(lambda x: x.to_numpy(), image)), candidate_labels=[classes]*len(image), **config)