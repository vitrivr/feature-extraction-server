
from feature_extraction_server.core.model import Model
import gc

class DinoV2Vits14(Model):

    def _load_model(self):
        global F, torch, np
        import torch.nn.functional as F
        import torch
        import torchvision.transforms as transforms
        import numpy as np
        
        self.dinov2_model = torch.hub.load('facebookresearch/dinov2', 'dinov2_vits14').eval()
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.dinov2_model = self.dinov2_model.to(self.device)
        self.dinov2_model.eval()

        # Image transformation
        self.transform_image = transforms.Compose([
            transforms.ToTensor(),
            transforms.Resize(244, antialias=True),
            transforms.CenterCrop(224),
            transforms.Normalize([0.5], [0.5])
        ])
    
    def batched_image_embedding(self, image, config={}):
        img = np.array([self.transform_image(x.to_numpy())[:3] for x in image])
        with torch.no_grad():
            gc.collect()
            return {"embedding":self.dinov2_model(torch.from_numpy(img)).tolist()}