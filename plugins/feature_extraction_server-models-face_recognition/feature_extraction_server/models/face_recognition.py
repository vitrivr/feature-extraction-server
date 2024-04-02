from feature_extraction_server.core.model import Model

class FaceRecognition(Model):
    def _load_model(self):
        global face_recognition
        import face_recognition

    def face_embedding(self, image, config={}):
        img = image.to_numpy()
        boxes = face_recognition.face_locations(img, model=config["detection_method"])
        encodings = face_recognition.face_encodings(img, boxes)
        return {"embedding":encodings}