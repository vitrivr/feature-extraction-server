from feature_extraction_server.core.model import Model

class OwlVitBasePatch32(Model):

    def _load_model(self):
        from transformers import pipeline

        checkpoint = "google/owlvit-base-patch32"
        self.detector = pipeline(model=checkpoint, task="zero-shot-object-detection")

    def batched_zero_shot_object_detection(self, image, classes, config={}):
        probabilites = self.detector(list(map(lambda x: x.to_numpy(), image)), candidate_labels=[classes]*len(image), **config)
        return {"probabilities":probabilites}