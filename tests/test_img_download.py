import os
import shutil
import requests

url = "https://ipfs.io/ipfs/QmR43AkgZRSCGHgiiBibo6v5JyC31ArgqgC1z1kCvzanWS/3402.png"
thumb_path = "spirit.png"

res = requests.get(url, stream = True)

if res.status_code == 200:
    with open(thumb_path, "wb") as f:
        shutil.copyfileobj(res.raw, f)
    print('Image sucessfully Downloaded: ', thumb_path)
else:
    print('Image Couldn\'t be retrieved')

#os.remove(thumb_path)
