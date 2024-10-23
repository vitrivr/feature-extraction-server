
from feature_extraction_server.core.model import Model
from simple_plugin_manager.settings import FlagSetting
import gc
import logging
logger = logging.getLogger(__name__)

def is_cuda_available():
    if not torch.cuda.is_available():
        return False
    try:
        # Try to perform a simple CUDA operation
        torch.zeros(1).to('cuda')
        return True
    except Exception:
        return False
class DinoV2Vits14(Model):

    def _load_model(self):
        global F, torch, np
        import torch.nn.functional as F
        import torch
        import torchvision.transforms as transforms
        import numpy as np
        
        no_cuda_setting = FlagSetting("NO_CUDA", "If set, the model will not use CUDA.")
        self.no_cuda = no_cuda_setting.get()
        
        self.dinov2_model = torch.hub.load('facebookresearch/dinov2', 'dinov2_vits14').eval()
        if is_cuda_available():
            if self.no_cuda:
                logger.debug("CUDA is available but not being used due to --no-cuda setting.")
                self.device = torch.device("cpu")
            else:
                logger.debug("CUDA is available and being used.")
                self.device = torch.device("cuda")
        else:
            logger.debug("CUDA is not available. Using CPU.")
            self.device = torch.device("cpu")
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