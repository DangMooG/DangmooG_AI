from bing_image_downloader import downloader

categories = [
    'luxury goods', 
    'clothing & fashion goods', 
    'beauty products', 
    'mobile devices', 
    'computers & PC', 
    'peripheral devices', 
    'small electronics', 
    'daily supplies', 
    'bags & accessories',   
    'shoes',
    'media entertainments',
    'furniture & household goods',
    'toys & hobby supplies',
    'sports & outdoor products',
    'DIY & gardem products',
    'stationery',
    'pet products',
    'textbooks',
    'bikes & bicycles'
    ]

for category in categories:
    downloader.download(category,limit=50, output_dir="./images",adult_filter_off=False)    
