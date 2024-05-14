
from feature_extraction_server.core.model import Model


class ClipVitLargePatch14(Model):

    def _load_model(self):
        global F, torch
        
        import torch
        from transformers import CLIPModel
        from transformers import AutoTokenizer, AutoProcessor
        import torch.nn.functional as F

        self.model = CLIPModel.from_pretrained("openai/clip-vit-large-patch14")
        self.processor = AutoProcessor.from_pretrained("openai/clip-vit-large-patch14")
        self.tokenizer = AutoTokenizer.from_pretrained("openai/clip-vit-large-patch14")
        
        self.model.eval()
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model.to(self.device)


    def batched_text_embedding(self, text, config={}):
        inputs = self.tokenizer(text, padding=True, return_tensors="pt")
        with torch.no_grad():
            outputs = self.model.get_text_features(**inputs, **config)
        outputs = F.normalize(outputs, p=2, dim=-1)
        return {"embedding":outputs.tolist()}

    def batched_image_embedding(self, image, config={}):
        inputs = self.processor(images=list(map(lambda x: x.to_numpy(), image)), return_tensors="pt")
        with torch.no_grad():
            outputs = self.model.get_image_features(**inputs, **config)
        
        outputs = F.normalize(outputs, p=2, dim=-1)
        return {"embedding":outputs.tolist()}


    def batched_zero_shot_image_classification(self, image, classes, config={}):
        inputs = self.processor(text=classes, images=list(map(lambda x: x.to_numpy(), image)), return_tensors="pt", padding=True)
        with torch.no_grad():
            outputs = self.model(**inputs)
        logits_per_image = outputs.logits_per_image # this is the image-text similarity score
        probs = logits_per_image.softmax(dim=1) # we can take the softmax to get the label probabilities
        return {"probabilities":probs.tolist()}