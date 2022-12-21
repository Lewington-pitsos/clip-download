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
                image_path = os.path.join('hd', path)
                img.save(image_path)
                os.remove(testpath)

                parts = image_path.split(".")
                parts.pop(len(parts)-1)
                parts.append("txt")
                captionpath = ".".join(parts)
                captionfile = open(captionpath,"w")
                captionfile.write(image_caption)
                captionfile.close()
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