from feature_extraction_server.core.model import Model

class EasyOcr(Model):

    def _load_model(self,):
        import easyocr
        self.reader = easyocr.Reader(['en'])

    def batched_optical_character_recognition(self, image, config={}):
        out = self.reader.readtext(image.to_numpy())
        text = " ".join([x[1] for x in out])
        return {"text":text}