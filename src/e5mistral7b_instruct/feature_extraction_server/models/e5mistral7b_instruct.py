
from feature_extraction_server.core.model import Model

def last_token_pool(last_hidden_states,
                 attention_mask):
    left_padding = (attention_mask[:, -1].sum() == attention_mask.shape[0])
    if left_padding:
        return last_hidden_states[:, -1]
    else:
        sequence_lengths = attention_mask.sum(dim=1) - 1
        batch_size = last_hidden_states.shape[0]
        return last_hidden_states[torch.arange(batch_size, device=last_hidden_states.device), sequence_lengths]

class E5mistral7bInstruct(Model):

    def _load_model(self):
        global torch, F, Tensor, AutoTokenizer, AutoModel
        import torch
        import torch.nn.functional as F

        from torch import Tensor
        from transformers import AutoTokenizer, AutoModel

        self.model = AutoModel.from_pretrained('intfloat/e5-mistral-7b-instruct')
        self.tokenizer = AutoTokenizer.from_pretrained('intfloat/e5-mistral-7b-instruct')

    def _embed(self, text):
        max_length = 4096
        batch_dict = self.tokenizer(text, max_length=max_length - 1, return_attention_mask=False, padding=False, truncation=True)
        batch_dict['input_ids'] = [input_ids + [self.tokenizer.eos_token_id] for input_ids in batch_dict['input_ids']]
        batch_dict = self.tokenizer.pad(batch_dict, padding=True, return_attention_mask=True, return_tensors='pt')
        
        outputs = self.model(**batch_dict)
        embeddings = last_token_pool(outputs.last_hidden_state, batch_dict['attention_mask'])
        return {"embedding":embeddings.tolist()}

    def batched_text_embedding(self, text, config={}):
        return self._embed(text)

    def batched_text_query_embedding(self, query, instruction, config={}):
        detailed_query = [f"Instruct: {instruction}\nQuery: {q}" for q in query]
        return self._embed(detailed_query)