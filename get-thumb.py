import sys
import requests
import urllib
import cv2
import json
import re
import numpy as np
import subprocess

def url_to_image(url):
    resp = urllib.request.urlopen(url)
    image = np.asarray(bytearray(resp.read()), dtype="uint8")
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)
    return image

def main():
    url = sys.argv[1]
    file_type = sys.argv[2]
    video_id = str(url.split("=", 1)[1]) # Split into arrary and get video id
    #Get YouTube Data API v3 Key here https://console.cloud.google.com
    get = requests.get('https://www.googleapis.com/youtube/v3/videos', params = {'id': video_id, 'part': 'contentDetails,statistics,snippet', 'key': 'INSERT DEVELOPER API KEY HERE'})    
    resp_dict = json.loads(get.content)
    title = resp_dict['items'][0]['snippet']['title']

    title = re.sub(r'[\\/*?:"<>|]'," ",title) # Replace illegal characters

    for i in range(0, len(title)):
             try:
                 title[i].encode("ascii")
             except:
                  title=title.replace(title[i]," ")

    title = title.encode('ascii',"ignore") # Has to encode it again into ASCII for some reaosn
    title = title.decode() # Finished string

    try:
        img = url_to_image('https://img.youtube.com/vi/'+video_id+'/maxresdefault.jpg')
        if str(file_type) == 'm4a':
            height = 720
            width = 720 # keep original width
            dim = (width, height)
            img = cv2.resize(img, dim)

    except: # Some videos do not have maxresdafult thumbnails, switch to best alternative
        img = url_to_image('https://img.youtube.com/vi/'+video_id+'/hqdefault.jpg')
        if str(file_type) == 'm4a':
            height = 360
            width = 360 
            dim = (width, height)
            img = cv2.resize(img, dim)
        
    cv2.imwrite(title + '.jpg', img)
    p = subprocess.run(['youtube-dl',url,'-f'+file_type]) # Run youtube-dl

if __name__ == "__main__":
    main()