import uvicorn
from fastapi import FastAPI, File, UploadFile
from application.components import predict, read_imagefile, translate_to_kr

app = FastAPI()
@app.post("/predict/image")
async def predict_api(file: UploadFile = File(...)):
    image = read_imagefile(await file.read())
    prediction = translate_to_kr(predict(image))
    return prediction

if __name__ == "__main__":
    uvicorn.run(app, debug=True)