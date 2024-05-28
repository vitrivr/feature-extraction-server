
from feature_extraction_server.core.model import Model
import time
import random

class BrokenModel(Model):

    def _load_model(self):
        pass


    def batched_text_embedding(self, text, config={}):
        # wait a second
        time.sleep(0.1)
        #flip a coin
        if random.random() < 0.5:
            return {"embedding": [[0]]}
        else:
            exit(1)