import requests

with open('1.jpg', 'wb') as f:
    img_req = requests.get('https://img.pic123456.com/girl/mfxy/122/03.jpg' ,stream=True)
    for chunk in img_req:
        f.write(chunk)
