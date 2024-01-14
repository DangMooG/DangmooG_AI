from io import BytesIO
import numpy as np
from brisque import BRISQUE


def get_alpha_score(img_path, is_url=False):
    obj = BRISQUE(url=is_url)
    if is_url:
        alpha = round(obj.score(img_path)/100, 3)
    else:
        img = read_imagefile(img_path)
        alpha = round(obj.score(img)/100, 3)
    
    return alpha

# def load_model():
#     model = tf.keras.applications.MobileNetV2(weights="imagenet")
#     return model

# def predict(image: Image.Image):
#     image = np.asarray(image.resize((224, 224)))[..., :3]
#     image = np.expand_dims(image, 0)
#     image = image / 127.5 - 1.0
#     result = decode_predictions(model.predict(image), 2)[0]
#     response = []
#     for i, res in enumerate(result):
#         resp = {}
#         resp["class"] = res[1]
#         resp["confidence"] = f"{res[2]*100:0.2f} %"
#         response.append(resp)
#     return response

# def translate_to_kr(str: str):
#     translator = googletrans.Translator()
#     return translator.translate(str, dest='ko')