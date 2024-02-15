from feature_extraction_server.core.model import Model

class EasyOcr(Model):

    def _load_model(self,):
        import easyocr
        self.reader = easyocr.Reader(['en'])

    def optical_character_recognition(self, image, config={}):
        results = []
        for img in image:
            out = self.reader.readtext(img.to_numpy())
            text = " ".join([x[1] for x in out])
            results.append(text)
        
        return {"text":results}