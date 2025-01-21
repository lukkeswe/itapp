import os
import requests
from bs4 import BeautifulSoup

def picture(baseUrl, index, folderName):
    # Folder where you want to save the downloaded images
    folder_path = folderName
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    
    if index < 10:
        extention = "img/0"
    else:
        extention = "img/"
        
    direct_image_url = baseUrl + extention + str(index) + ".png"
        
    response = requests.get(direct_image_url)
    
    if response.status_code == 200 and response.content:
        direct_image = requests.get(direct_image_url).content
        img_name = os.path.join(folder_path, direct_image_url.split('/')[-1])
        with open(img_name, 'wb') as img_file:
            img_file.write(direct_image)
        print(f'Downloaded {img_name}')
    
    for i in range(1, 11):
        direct_image_url = baseUrl + extention + str(index) + "_" + str(i) + ".png"
        
        response = requests.get(direct_image_url)
        
        if response.status_code == 200 and response.content:
            direct_image = requests.get(direct_image_url).content
            img_name = os.path.join(folder_path, direct_image_url.split('/')[-1])
            with open(img_name, 'wb') as img_file:
                img_file.write(direct_image)
            print(f'Downloaded {img_name}')
            
    answer_extension = ["a", "i", "u", "e"]
    for answer in answer_extension:
        direct_image_url = baseUrl + extention + str(index) + answer + ".png"
        
        response = requests.get(direct_image_url)
        
        if response.status_code == 200 and response.content:
            direct_image = requests.get(direct_image_url).content
            img_name = os.path.join(folder_path, direct_image_url.split('/')[-1])
            with open(img_name, 'wb') as img_file:
                img_file.write(direct_image)
            print(f'Downloaded {img_name}')
        

# for i in range(1, 101):
#     picture("https://www.itpassportsiken.com/kakomon/27_aki/", i, "27-aki")
    
# print("Finnished download")