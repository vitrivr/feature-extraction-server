
from feature_extraction_server.core.model import Model
import gc

class OpenClipVitB32(Model):

    def _load_model(self):
        global F, torch, np
        import torch.nn.functional as F
        import torch
        import open_clip
        import numpy as np
        
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        model, _, preprocess = open_clip.create_model_and_transforms('xlm-roberta-base-ViT-B-32',
                                                                    pretrained='laion5b_s13b_b90k')
        self.model = model.to(self.device)
        self.model.eval()
        self.tokenizer = open_clip.get_tokenizer('xlm-roberta-base-ViT-B-32')
        self.transform_image = preprocess


    def batched_text_embedding(self, text, config={}):
        text = self.tokenizer(text).to(self.device)
        with torch.no_grad():
            text_features = F.normalize(self.model.encode_text(text), p=2, dim=-1)
            gc.collect()
            return {"embedding":text_features.tolist()}
    
    def batched_image_embedding(self, image, config={}):
        img = np.array([self.transform_image(x.to_pillow())[:3] for x in image])
        with torch.no_grad():
            image_features = F.normalize(self.model.encode_image(torch.from_numpy(img)), p=2, dim=-1)
            gc.collect()
            return {"embedding":image_features.tolist()}
    
    def batched_zero_shot_image_classification(self, image, classes, config={}):
        tokenized_classes = self.tokenizer(classes).to(self.device)
        img = np.array([self.transform_image(x.to_pillow())[:3] for x in image])
        
        with torch.no_grad():
            image_features = F.normalize(self.model.encode_image(torch.from_numpy(img)), p=2, dim=-1)
            text_features = F.normalize(self.model.encode_text(tokenized_classes), p=2, dim=-1)
            
            return {"probabilities":(image_features @ text_features.T).softmax(dim=-1).tolist()}
            

