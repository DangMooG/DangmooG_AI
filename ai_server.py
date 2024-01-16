import os
import json

from PIL import Image
from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from application.nvshopping import get_search_url, get_result_page, get_mean_price_nv
from application.joongna import scrap_joogna_price
from application.llm_agent import get_product_name, get_product_name_with_description


from brisque import BRISQUE
from dotenv import load_dotenv
import tempfile

load_dotenv()
openai_api_key = os.environ.get('OPEN_AI_API_KEY')  # openai api key
client_id = os.environ.get('NAVER_ID')
client_secret = os.environ.get('NAVER_SECRET')
obj = BRISQUE()
def set_config(config_path):
    with open(config_path, 'r') as config_file:
        config_data = json.load(config_file)

    db_config = config_data.get('ndev_config', {})

    client_id = db_config.get('client_id', '')
    client_secret = db_config.get('client_secret', '')

    return client_id, client_secret


def get_rec_price(upper, lower, alpha) -> int:
    recommend_price = (1 - alpha) * upper + alpha * lower
    return int(round(recommend_price, -1))


def get_results_list(upper, recommend, lower) -> list:
    results = set([round(upper, -1), round(recommend, -1), round(lower, -1)])
    results = sorted(list(results), reverse=True)
    results = list(map(int, list(results)))
    return results


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


@app.post(
    "/predict/get_price",
    name="가격 추천 획득 beta",
    description="글의 제목을 title에 넣고, 게시물의 대표사진 1개를 photo 항목에 전송하면 됩니다."
                "\n\n"
                "결과는 가격의 리스트 형태로 반환됩니다."
)
async def predict_api(title: str, photo: UploadFile = File(...)) -> list:
    product = get_product_name(
        title=title,
        openai_api_key=openai_api_key
    )  # 상품명 - 검색가능한 형태

    image = Image.open(photo.file)
    alpha = round(obj.score(image) / 100, 3)


    url = get_search_url(product, 1, 5)
    result = get_result_page(url, client_id, client_secret)
    new_mean_price = get_mean_price_nv(result)  # 새상품 기준 평균가

    trend_price, lower_price = scrap_joogna_price(product)
    if trend_price != 0:
        if new_mean_price >= trend_price:
            upper_price = get_rec_price(new_mean_price, trend_price, alpha)
        else:
            upper_price = new_mean_price * 0.9

    else:
        upper_price = get_rec_price(new_mean_price, new_mean_price * 0.6, alpha)
        lower_price = new_mean_price * 0.6

    recommend_price = get_rec_price(upper_price, lower_price, alpha)
    results = get_results_list(upper_price, recommend_price, lower_price)

    return results


@app.post(
    "/predict/get_price",
    name="가격 추천 획득 beta version 2",
    description="글의 제목을 title에 넣고, 추가로 내용을 description에 넣고, 게시물의 대표사진 1개를 photo 항목에 전송하면 됩니다."
                "\n\n"
                "결과는 가격의 리스트 형태로 반환됩니다."
)
async def predict_api(title: str, description: str, photo: UploadFile = File(...)) -> list:
    product = get_product_name_with_description(
        title=title,
        description=description,
        openai_api_key=openai_api_key
    )  # 상품명 - 검색가능한 형태

    image = Image.open(photo.file)
    alpha = round(obj.score(image) / 100, 3)


    url = get_search_url(product, 1, 5)
    result = get_result_page(url, client_id, client_secret)
    new_mean_price = get_mean_price_nv(result)  # 새상품 기준 평균가

    trend_price, lower_price = scrap_joogna_price(product)
    if trend_price != 0:
        if new_mean_price >= trend_price:
            upper_price = get_rec_price(new_mean_price, trend_price, alpha)
        else:
            upper_price = new_mean_price * 0.9

    else:
        upper_price = get_rec_price(new_mean_price, new_mean_price * 0.6, alpha)
        lower_price = new_mean_price * 0.6

    recommend_price = get_rec_price(upper_price, lower_price, alpha)
    results = get_results_list(upper_price, recommend_price, lower_price)

    return results