from mplug_owl.modeling_mplug_owl import MplugOwlForConditionalGeneration
from mplug_owl.tokenization_mplug_owl import MplugOwlTokenizer
from mplug_owl.processing_mplug_owl import MplugOwlImageProcessor, MplugOwlProcessor
import torch
from utils import batch

pretrained_ckpt = 'MAGAer13/mplug-owl-llama-7b'
model = MplugOwlForConditionalGeneration.from_pretrained(
    pretrained_ckpt,
    torch_dtype=torch.bfloat16,
)
image_processor = MplugOwlImageProcessor.from_pretrained(pretrained_ckpt)
tokenizer = MplugOwlTokenizer.from_pretrained(pretrained_ckpt)
processor = MplugOwlProcessor(image_processor, tokenizer)

defaults = {}

# from PIL import Image
# images = [Image.open(_) for _ in image_list]
# inputs = processor(text=prompts, images=images, return_tensors='pt')
# inputs = {k: v.bfloat16() if v.dtype == torch.float else v for k, v in inputs.items()}
# inputs = {k: v.to(model.device) for k, v in inputs.items()}
# with torch.no_grad():
#     res = model.generate(**inputs, **generate_kwargs)
# sentence = tokenizer.decode(res.tolist()[0], skip_special_tokens=True)


def conditional_caption(image, text, inference_args={}):
    # Set defaults if not provided
    args = defaults.copy()
    args.update(inference_args)
    
    inputs = processor(images=image, text=[text]*len(image), return_tensors="pt")
    inputs = {k: v.bfloat16() if v.dtype == torch.float else v for k, v in inputs.items()}
    inputs = {k: v.to(model.device) for k, v in inputs.items()}
    with torch.no_grad():
        output_ids = model.generate(**inputs,  **args)
    preds = processor.batch_decode(True, output_ids)
    preds = [pred.strip() for pred in preds]
    return list(batch(preds, len(preds)//len(image)))