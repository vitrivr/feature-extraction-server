from collections import OrderedDict
import hashlib
from feature_extraction_server.core.model import Model
from simple_plugin_manager.settings import FlagSetting
import numpy as np
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

class LRUCache:
    def __init__(self, maxsize=100):
        self.cache = OrderedDict()
        self.maxsize = maxsize

    def cache_get(self, key):
        try:
            value = self.cache.pop(key)
            # Re-insert to mark as most recently used
            self.cache[key] = value
            return value
        except KeyError:
            return None

    def cache_set(self, key, value):
        try:
            self.cache.pop(key)
        except KeyError:
            if len(self.cache) >= self.maxsize:
                self.cache.popitem(last=False)
        self.cache[key] = value

class ClipVitLargePatch14(Model):

    def _load_model(self):
        global F, torch
        
        import torch
        from transformers import CLIPModel
        from transformers import AutoTokenizer, AutoProcessor
        import torch.nn.functional as F
        
        no_cuda_setting = FlagSetting("NO_CUDA", "If set, the model will not use CUDA.")
        self.no_cuda = no_cuda_setting.get()

        self.model = CLIPModel.from_pretrained("openai/clip-vit-large-patch14")
        self.processor = AutoProcessor.from_pretrained("openai/clip-vit-large-patch14")
        self.tokenizer = AutoTokenizer.from_pretrained("openai/clip-vit-large-patch14")
        
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

        # Initialize caches
        self.text_cache = LRUCache(maxsize=100)
        self.image_cache = LRUCache(maxsize=100)

    def serialize_image(self, image):
        # Convert image to bytes and hash it for a consistent cache key
        image_array = np.array(image.to_pillow())
        image_bytes = image_array.tobytes()
        image_hash = hashlib.md5(image_bytes).hexdigest()
        return image_hash

    def batched_text_embedding(self, text, config={}):
        results = [None] * len(text)
        uncached_texts = []
        uncached_indices = []

        for idx, t in enumerate(text):
            cached_result = self.text_cache.cache_get(t)
            if cached_result is not None:
                results[idx] = cached_result
            else:
                uncached_texts.append(t)
                uncached_indices.append(idx)

        if uncached_texts:
            inputs = self.tokenizer(uncached_texts, padding=True, return_tensors="pt", truncation=True).to(self.device)
            with torch.no_grad():
                outputs = self.model.get_text_features(**inputs)
            outputs = F.normalize(outputs, p=2, dim=-1).cpu().tolist()

            for i, idx in enumerate(uncached_indices):
                embedding = outputs[i]
                self.text_cache.cache_set(text[idx], embedding)
                results[idx] = embedding

        return {"embedding": results}

    def batched_image_embedding(self, image, config={}):
        results = [None] * len(image)
        uncached_images = []
        uncached_indices = []

        for idx, img in enumerate(image):
            image_key = self.serialize_image(img)
            cached_result = self.image_cache.cache_get(image_key)
            if cached_result is not None:
                results[idx] = cached_result
            else:
                uncached_images.append(img)
                uncached_indices.append(idx)

        if uncached_images:
            inputs = self.processor(images=[img.to_pillow() for img in uncached_images], return_tensors="pt").to(self.device)
            with torch.no_grad():
                outputs = self.model.get_image_features(**inputs)
            outputs = F.normalize(outputs, p=2, dim=-1).cpu().tolist()

            for i, idx in enumerate(uncached_indices):
                embedding = outputs[i]
                image_key = self.serialize_image(image[idx])
                self.image_cache.cache_set(image_key, embedding)
                results[idx] = embedding

        return {"embedding": results}

    def batched_zero_shot_image_classification(self, image, classes, config={}):
        # Cache image embeddings
        image_embeddings = self.batched_image_embedding(image)["embedding"]
        
        # Cache class embeddings
        class_embeddings = self.batched_text_embedding(classes)["embedding"]

        # Convert embeddings back to tensors
        image_tensors = torch.tensor(image_embeddings, device=self.device)
        class_tensors = torch.tensor(class_embeddings, device=self.device)

        # Compute similarity scores
        with torch.no_grad():
            logits_per_image = image_tensors @ class_tensors.T
            probs = logits_per_image.softmax(dim=1)

        return {"probabilities": probs.cpu().tolist()}
