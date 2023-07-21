from transformers import pipeline

checkpoint = "google/owlvit-base-patch32"
detector = pipeline(model=checkpoint, task="zero-shot-object-detection")


def zero_shot_object_detection(image, classes, config={}):
    return detector(image, candidate_labels=[classes]*len(image), **config)