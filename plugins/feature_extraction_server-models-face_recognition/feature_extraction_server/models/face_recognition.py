def load_model():
    global face_recognition
    import face_recognition

def face_embedding(image, config={}):
    result = []
    for img in image:
        img = img.to_numpy()
        boxes = face_recognition.face_locations(img, model=config["detection_method"])
        encodings = face_recognition.face_encodings(img, boxes)
        result.append(encodings)
    return result