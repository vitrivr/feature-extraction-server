from functools import lru_cache
from feature_extraction_server.core.model import Model
from simple_plugin_manager.services.settings_manager import SettingsManager
from simple_plugin_manager.settings import FlagSetting
import logging
logger = logging.getLogger(__name__)

def last_token_pool(last_hidden_states, attention_mask):
    left_padding = (attention_mask[:, -1].sum() == attention_mask.shape[0])
    if left_padding:
        return last_hidden_states[:, -1]
    else:
        sequence_lengths = attention_mask.sum(dim=1) - 1
        batch_size = last_hidden_states.shape[0]
        return last_hidden_states[torch.arange(batch_size, device=last_hidden_states.device), sequence_lengths]

def is_cuda_available():
    if not torch.cuda.is_available():
        return False
    try:
        # Try to perform a simple CUDA operation
        torch.zeros(1).to('cuda')
        return True
    except Exception:
        return False

class E5mistral7bInstruct(Model):

    def _load_model(self):
        global torch, F, Tensor, AutoTokenizer, AutoModel
        import torch
        import torch.nn.functional as F
        from torch import Tensor
        from transformers import AutoTokenizer, AutoModel
        
        no_cuda_setting = FlagSetting("NO_CUDA", "If set, the model will not use CUDA.")
        self.no_cuda = no_cuda_setting.get()

        self.model = AutoModel.from_pretrained('intfloat/e5-mistral-7b-instruct')
        self.tokenizer = AutoTokenizer.from_pretrained('intfloat/e5-mistral-7b-instruct')
        
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

    @lru_cache(maxsize=100)
    def _embed(self, text_tuple):
        text = list(text_tuple)  # Convert tuple back to list for processing
        max_length = 4096
        batch_dict = self.tokenizer(text, max_length=max_length - 1, return_attention_mask=False, padding=False, truncation=True)
        batch_dict['input_ids'] = [input_ids + [self.tokenizer.eos_token_id] for input_ids in batch_dict['input_ids']]
        batch_dict = self.tokenizer.pad(batch_dict, padding=True, return_attention_mask=True, return_tensors='pt')
        with torch.no_grad():
            outputs = self.model(**batch_dict)
        embeddings = last_token_pool(outputs.last_hidden_state, batch_dict['attention_mask'])
        embeddings = F.normalize(embeddings, p=2, dim=-1)
        return {"embedding": embeddings.tolist()}

    def batched_text_embedding(self, text, config={}):
        return self._embed(tuple(text))  # Convert list to tuple for caching

    def batched_text_query_embedding(self, query, instruction, config={}):
        detailed_query = [f"Instruct: {instruction}\nQuery: {q}" for q in query]
        return self._embed(tuple(detailed_query))  # Convert list to tuple for caching
