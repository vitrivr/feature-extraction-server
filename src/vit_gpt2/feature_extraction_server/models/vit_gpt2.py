from feature_extraction_server.core.model import Model
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

class VitGpt2(Model):


    def _load_model(self):
        global torch, batch
        import torch
        from transformers import VisionEncoderDecoderModel, ViTImageProcessor, AutoTokenizer
        from feature_extraction_server.core.utils import batch

        # Load the model, tokenizer and feature extractor outside the endpoint
        self.model = VisionEncoderDecoderModel.from_pretrained("nlpconnect/vit-gpt2-image-captioning")
        self.feature_extractor = ViTImageProcessor.from_pretrained("nlpconnect/vit-gpt2-image-captioning")
        self.tokenizer = AutoTokenizer.from_pretrained("nlpconnect/vit-gpt2-image-captioning")

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

    # Default values for max_length and num_beams
    defaults = {}  #for more info on these args (and additional args), see https://huggingface.co/docs/transformers/main_classes/text_generation
        

    def batched_image_captioning(self, image, config={}):
        pixel_values = self.feature_extractor(images=list(map(lambda x: x.to_numpy(), image)), return_tensors="pt").pixel_values
        pixel_values = pixel_values.to(self.device)

        # Set defaults if not provided
        args = self.defaults.copy()
        args.update(config)
        with torch.no_grad():
            output_ids = self.model.generate(pixel_values, **args)
        preds = self.tokenizer.batch_decode(output_ids, skip_special_tokens=True)
        preds = [pred.strip() for pred in preds]
        batched =list(batch(preds, len(preds)//len(image)))
        return {"caption":[captions[0] for captions in batched]}