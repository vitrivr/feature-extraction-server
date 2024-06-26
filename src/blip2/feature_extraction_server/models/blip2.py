
from feature_extraction_server.core.model import Model
from simple_plugin_manager.settings import FlagSetting


class Blip2(Model):
    
    def setup(self):
        pass
    def _load_model(self):
        global torch, batch
        import torch
        from transformers import Blip2Processor, Blip2ForConditionalGeneration
        from feature_extraction_server.core.utils import batch
        
        no_cuda_setting = FlagSetting("NO_CUDA", "If set, the model will not use CUDA.")
        self.no_cuda = no_cuda_setting.get()

        self.defaults = {}

        self.device = "cuda" if torch.cuda.is_available() and not self.no_cuda else "cpu"

        self.processor = Blip2Processor.from_pretrained("Salesforce/blip2-opt-2.7b")
        self.condgenmodel = Blip2ForConditionalGeneration.from_pretrained(
            "Salesforce/blip2-opt-2.7b", torch_dtype=torch.float
        )
        self.condgenmodel.to(self.device)
        self.condgenmodel.eval()

    def batched_conditional_image_captioning(self, image, text, config={}):
        
        # Set defaults if not provided
        args = self.defaults.copy()
        args.update(config)
        
        image_tensor = list(map(lambda x: x.to_numpy(), image))
        
        inputs = self.processor(images=image_tensor, text=text, return_tensors="pt", padding=True)
        inputs = {k: v.to(self.condgenmodel.device) for k, v in inputs.items()}
        with torch.no_grad():
            output_ids = self.condgenmodel.generate(**inputs,  **args)
        preds = self.processor.batch_decode(output_ids, skip_special_tokens=True)
        preds = [pred.strip() for pred in preds]
        batched =list(batch(preds, len(preds)//len(image)))
        return {"caption":[captions[0] for captions in batched]}


    def batched_image_captioning(self, image, config):
        # Set defaults if not provided
        args = self.defaults.copy()
        args.update(config)
        
        image_tensor = list(map(lambda x: x.to_numpy(), image))
        
        inputs = self.processor(images=image_tensor, return_tensors="pt", padding=True)
        inputs = {k: v.to(self.condgenmodel.device) for k, v in inputs.items()}
        with torch.no_grad():
            output_ids = self.condgenmodel.generate(**inputs,  **args)
        preds = self.processor.batch_decode(output_ids, skip_special_tokens=True)
        preds = [pred.strip() for pred in preds]
        batched =list(batch(preds, len(preds)//len(image)))
        return {"caption":[captions[0] for captions in batched]}