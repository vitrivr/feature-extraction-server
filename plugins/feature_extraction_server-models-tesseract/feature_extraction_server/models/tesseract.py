from feature_extraction_server.core.model import Model
class Tesseract(Model):

    def _load_model(self):
        global pytesseract
        import pytesseract

    def optical_character_recognition(self, image, config):
        # config is not used currently
        text = pytesseract.image_to_string(image.to_numpy(), config="", output_type=pytesseract.Output.DICT)["text"]
        # text = "\n".join([t for t in text if t.strip()])
        return {"text": text}