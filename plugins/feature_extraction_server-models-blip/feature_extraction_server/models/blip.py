

from feature_extraction_server.core.model import Model


class Blip(Model):

    def _load_model(self):
        global torch, batch 
        
        from transformers import BlipProcessor, BlipForConditionalGeneration
        import torch
        from feature_extraction_server.core.utils import batch

        self.processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
        self.model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

        self.defaults = {}
        self.processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
        self.model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")


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