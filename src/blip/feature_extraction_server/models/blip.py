

from feature_extraction_server.core.model import Model
from simple_plugin_manager.services.settings_manager import SettingsManager
from simple_plugin_manager.settings import FlagSetting
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
    

class Blip(Model):

    def _load_model(self):
        global torch, batch 
        
        no_cuda_setting = FlagSetting("NO_CUDA", "If set, the model will not use CUDA.")
        self.no_cuda = no_cuda_setting.get()
        
        from transformers import BlipProcessor, BlipForConditionalGeneration
        import torch
        from feature_extraction_server.core.utils import batch

        self.defaults = {}
        self.processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
        self.model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")
        
        self.model.eval()
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
        
        self.model.to(self.device)

    def batched_image_captioning(self, image, config={}):
        # Set defaults if not provided
        args = self.defaults.copy()
        args.update(config)
        inputs = self.processor(list(map(lambda x: x.to_numpy(), image)), return_tensors="pt")
        inputs = {k: v.to(self.model.device) for k, v in inputs.items()}
        with torch.no_grad():
            output_ids = self.model.generate(**inputs, **config)
        preds = self.processor.batch_decode(output_ids, skip_special_tokens=True)
        preds = [pred.strip() for pred in preds]
        batched =list(batch(preds, len(preds)//len(image)))
        return {"caption":[captions[0] for captions in batched]}

    def batched_conditional_image_captioning(self, image, text, config={}):
        # Set defaults if not provided
        args = self.defaults.copy()
        args.update(config)
        
        inputs = self.processor(list(map(lambda x: x.to_numpy(), image)), text=text, return_tensors="pt", padding=True)
        inputs = {k: v.to(self.model.device) for k, v in inputs.items()}
        with torch.no_grad():
            output_ids = self.model.generate(**inputs,  **args)
        preds = self.processor.batch_decode(output_ids, skip_special_tokens=True)
        preds = [pred.strip() for pred in preds]
        batched =list(batch(preds, len(preds)//len(image)))
        return {"caption":[captions[0] for captions in batched]}