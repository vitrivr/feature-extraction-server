import easyocr
reader = easyocr.Reader(['en'])

def optical_character_recognition(image, config={}):
    results = []
    for img in image:
        out = reader.readtext(img.to_numpy())
        text = " ".join([x[1] for x in out])
        results.append(text)
    
    return results