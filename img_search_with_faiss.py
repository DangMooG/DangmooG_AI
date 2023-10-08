import tensorflow as tf
import tensorflow_hub as hub
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
import cv2
import faiss
import os
os.environ['KMP_DUPLICATE_LIB_OK']='True'

from tqdm import tqdm
import supervision as sv
import csv

# Load MobileNetV2 model from TensorFlow Hub
model_url = "https://tfhub.dev/google/tf2-preview/mobilenet_v2/classification/4"
model = hub.load(model_url)

# Initialize FAISS Index
index_dimension = 1001
index = faiss.IndexFlatL2(index_dimension)  # L2 distance

# functions to embed images and add them to FAISS indexes
def embed_and_add_to_index(image_path, model, faiss_index):
    img = image.load_img(image_path, target_size=(224, 224))
    img_array = image.img_to_array(img)
    img_array = preprocess_input(img_array)
    img_tensor = tf.expand_dims(img_array, axis=0)
    
    # create embeddings
    embedding = model(img_tensor).numpy().astype('float32')

    # add embedded vectors to FAISS index
    faiss_index.add(embedding)

index_path = './data/train/train.index'

if os.path.exists(index_path):
    index = faiss.read_index(index_path)
    file_names = []
    with open('./data/train/file_names.csv', 'r') as f:
        rea = csv.reader(f)
        for row in rea:
            file_names.append(row)
else:
    file_names = []
    path = './data/train'
    for root, directories, files in os.walk(path):
            for file in tqdm(files):
                if not os.path.isfile(os.path.join(root, file)):
                    continue

                if file.endswith('.jpg'):
                    file_path = os.path.join(root, file)
                    try:
                        embed_and_add_to_index(file_path, model, index)
                        file_names.append(file_path)
                    except:
                        print(file_path)
                        os.remove(file_path)
    faiss.write_index(index, './data/train/train.index')
    with open('./data/train/file_names.csv', 'w') as f:
        writer = csv.writer(f)
        for file_name in file_names:
            writer.writerow([file_name])

# query image
query_image_path = "./data/test/shoes_example.jpg"
query_img = image.load_img(query_image_path, target_size=(224, 224))
query_img_array = image.img_to_array(query_img)
query_img_array = preprocess_input(query_img_array)
query_img_tensor = tf.expand_dims(query_img_array, axis=0)

query_embedding = model(query_img_tensor).numpy()

# similarity search with FAISS index
k = 2
distances, indices = index.search(query_embedding, k)

print("Top {} 가장 유사한 이미지 인덱스: {}".format(k, indices))
print("Top {} 가장 유사한 이미지 거리: {}".format(k, distances))

# display
print([file_names[i][0] for i in indices[0]])

# images = [cv2.imread(file_names[i][0]) for i in indices[0]]

# sv.plot_images_grid(images, (k, k))