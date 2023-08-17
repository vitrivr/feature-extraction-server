import pytesseract

def optical_character_recognition(image, config):
    if config is None:
        config = ""
    results = []
    for img in image:
        results.append(pytesseract.image_to_data(img.to_numpy(), config=config, output_type=pytesseract.Output.DICT))
    return results