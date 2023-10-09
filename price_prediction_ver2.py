import numpy as np
import csv

import requests
from bs4 import BeautifulSoup
import re

import tensorflow as tf
import tensorflow_hub as tfhub
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input

import faiss

import os
os.environ['KMP_DUPLICATE_LIB_OK']='True'

from tqdm import tqdm

def load_im_model(model_url):
    model = tfhub.load(model_url)
    return model

def get_embedding(image_path, model):
    img = image.load_img(image_path, target_size=(224, 224))
    img_array = image.img_to_array(img)
    img_array = preprocess_input(img_array)
    img_tensor = tf.expand_dims(img_array, axis=0)

    img_embedding = model(img_tensor).numpy().astype('float32')
    
    return img_embedding

def make_vector_db(image_folder_path, model, faiss_index, index_file_path, csv_name='temp.csv'):
    file_list = []
    faill_list = []
    for root, _, files in os.walk(image_folder_path):
        for file in tqdm(files):
            file_path = os.path.join(root, file)
            if not os.path.isfile(file_path):
                print(f'ERROR: {file} is not a file.')
                faill_list.append(file_path)
                continue
            try:
                embedding = get_embedding(file_path, model)
                faiss_index.add(embedding)
                file_list.append(file_path)
            except:
                print(f"ERROR: {file} can't be added to index.")
                faill_list.append(file_path)
                
    faiss.write_index(faiss_index, index_file_path)
    with open(os.path.join(root, csv_name), 'w') as f:
        writer = csv.writer(f)
        for file_path in file_list:
            writer.writerow([file_path])
    return file_list, faill_list

def find_sim_items(k:int, query:np.array, index) -> list:
    distances, indices = index.search(query, k)
    return distances, indices

if __name__ == '__main__':
    model_url = "https://tfhub.dev/google/tf2-preview/mobilenet_v2/classification/4"
    model = load_im_model(model_url)
    k = 3
    
    data_folder_path = './data/train'
    query_image_path = './data/test/shoes.jpg'
    index_file_path = os.path.join(data_folder_path, 'temp.index')
    
    if os.path.exists(index_file_path):
        print('FAISS Index already exist.\n###Start Index Searching###')
        index = faiss.read_index(index_file_path)
    else:
        print("###Start making Index###")
        # Initialize FAISS Index
        index_dimension = 1001
        index = faiss.IndexFlatL2(index_dimension)  # L2 distance
        file_list, fail_list = make_vector_db(data_folder_path, model, index, index_file_path, csv_name='temp.csv')
    
    query_embedding = get_embedding(query_image_path, model)
    
    distances, indices = find_sim_items(k, query_embedding, index)
    
    print("Top {} 가장 유사한 이미지 인덱스: {}".format(k, indices))
    print("Top {} 가장 유사한 이미지 거리: {}".format(k, distances))

    # display
    print([file_list[i][0] for i in indices[0]])