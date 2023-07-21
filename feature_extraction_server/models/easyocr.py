import easyocr
reader = easyocr.Reader(['en'])
import numpy as np

def optical_character_recognition(image, config={}):
    results = []
    for img in image:
        out = reader.readtext(np.asarray(img))
        text = " ".join([x[1] for x in out])
        results.append(text)
    
    return results