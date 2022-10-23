import json
import requests 
import os
from PIL import Image

input_file = "clipsubset.json"

with open(input_file, encoding="utf8") as f:
    data = json.load(f)

count = 0
testpath = "tst.jpg"

for row in data:
    image_url = row['url']
    try:

        response = requests.get(image_url, stream = True)

        if response.status_code == 200:
            try:
                img = Image.open(response.raw)
                path = f'{count}.{img.format}'
                img.save(os.path.join(testpath))

                img = Image.open(testpath)
                img.verify()

                img = Image.open(testpath)
                img.save(os.path.join('hd', path))
                os.remove(testpath)

                print('Image sucessfully Downloaded')
                count+=1
            except Exception as e:
                if "seek" in str(e):
                    raise(e)
                print("encountered exception when reading image data from url", e)              
        else:
            print('Image Couldn\'t be retreived')
    except Exception as e:
        print("encountered connection error", e) 