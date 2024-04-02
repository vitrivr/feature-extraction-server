from feature_extraction_server.core.model import Model
class Tesseract(Model):

    def _load_model(self):
        global pytesseract
        import pytesseract

    def optical_character_recognition(self, image, config):
        if config is None:
            config = ""
        return {"text":pytesseract.image_to_data(image.to_numpy(), config=config, output_type=pytesseract.Output.DICT)}