import urllib.request
import json
import numpy as np

def get_search_url(searchText, startNum, dispNum, apiNode='shop'):
    base_url = "https://openapi.naver.com/v1/search"
    node="/"+apiNode+".json"
    param_query="?query="+urllib.parse.quote(searchText)
    param_start="&start="+str(startNum)
    param_disp="&display="+str(dispNum)
    
    return base_url+node+param_query+param_start+param_disp

def get_result_page(url, client_id, client_secret):
    request=urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id",client_id)
    request.add_header("X-Naver-Client-Secret",client_secret)
    response = urllib.request.urlopen(request)
    
    rescode = response.getcode()
    
    if(rescode==200):
        return json.loads(response.read().decode('utf-8'))
    else:
        return print("Error Code:" + rescode)

def get_mean_price_nv(result: json):
    price_list = []
    for item in result['items']:
        price_list.append(int(item['lprice']))

    mean_price = np.mean(price_list)
    return int(mean_price)

if __name__=='__main__':
    with open('config.json', 'r') as config_file:
        config_data = json.load(config_file)

    db_config = config_data.get('ndev_config', {})

    client_id = db_config.get('client_id', '')
    client_secret = db_config.get('client_secret', '')
    
    url = get_search_url('비타민',1,5)
    result = get_result_page(url,client_id,client_secret)
    
    print(get_mean_price_nv(result))