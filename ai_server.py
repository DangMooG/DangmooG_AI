from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from application.components import predict, read_imagefile, translate_to_kr
from price_prediction_mvp import *

app = FastAPI(title="Dangmuzi-AI", debug=True)

origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/predict/what_item_image")
async def predict_api(file: UploadFile = File(...)):
    image = read_imagefile(await file.read())
    prediction = translate_to_kr(predict(image)[0]["class"].replace("_", " "))
    return prediction.text


@app.post("/predict/price_with_image")
async def predict_api(file: UploadFile = File(...)):
    image = read_imagefile(await file.read())
    prediction = translate_to_kr(predict(image)[0]["class"].replace("_", " "))
    product = prediction.text
    alpha = get_brisque_score(image)
    trend_price, lower_price = scrapp_joogna(product)
    recommend_price = get_rec_price(trend_price, lower_price, alpha)
    results = get_results_list(trend_price, recommend_price, lower_price)
    return results

