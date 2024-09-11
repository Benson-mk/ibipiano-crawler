import requests
import json
import pandas as pd
import os
from concurrent.futures import ThreadPoolExecutor
import subprocess

# Define the API URL and the query parameters
url = 'https://www.ibipiano.com/_api/wix-ecommerce-storefront-web/api'
params = {
    'o': 'getData',
    's': 'WixStoresWebClient',
    'q': 'query,getData($externalId:String!,$compId:String,$mainCollectionId:String,$limit:Int!,$sort:ProductSort,$filters:ProductFilters,$offset:Int){appSettings(externalId:$externalId){widgetSettings}catalog{category(compId:$compId,categoryId:$mainCollectionId){id,name,productsWithMetaData(limit:$limit,onlyVisible:true,sort:$sort,filters:$filters,offset:$offset){list{id,name,media{url,mediaType}}totalCount}}allProductsCategoryId}}',
    'v': '{"externalId":"c34fd0fc-90b2-45ea-933b-288c45a2065a","compId":"TPASection_l569h06m","limit":500,"sort":null,"filters":null,"offset":0,"withOptions":false,"withPriceRange":false,"mainCollectionId":null}'
}
# Headers (including referer and user-agent)
headers = {
    'Referer': 'https://www.ibipiano.com/_partials/wix-thunderbolt/dist/clientWorker.e98266c5.bundle.min.js',
    'DNT': '1',
    'X-XSRF-TOKEN': '1726046194|_-w3ofkB26Tj',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
    'Authorization': 'NTBYso_Aa8XGMmtT1kk-c5to88ppJmiLU-nvquO_TRU.eyJpbnN0YW5jZUlkIjoiM2E4YTliNzYtMzU2My00NDFiLTg5NzgtN2VlNjI4YTJjMGFkIiwiYXBwRGVmSWQiOiIxMzgwYjcwMy1jZTgxLWZmMDUtZjExNS0zOTU3MWQ5NGRmY2QiLCJtZXRhU2l0ZUlkIjoiZTk1OGU3NTItZTA2ZS00MmJkLTkwYzItODAyZDBlMWI5ZTMxIiwic2lnbkRhdGUiOiIyMDI0LTA5LTExVDA5OjE2OjM0LjAwMVoiLCJ2ZW5kb3JQcm9kdWN0SWQiOiJzdG9yZXNfc2lsdmVyIiwiZGVtb01vZGUiOmZhbHNlLCJhaWQiOiJkNzFkNWE1My0xMmE4LTRkOWQtYTk3ZC1iYWFkZDJkMzllYmYiLCJiaVRva2VuIjoiZDNkMjdjMjQtZDUwZC0wNmE2LTE5YmEtZmVjYjI2Yjk1ZTljIiwic2l0ZU93bmVySWQiOiI4NjQ5NmRkMy1kZDIyLTRjNjctODhkOC0zY2E1ODNiMGZiNTYifQ',
    'Content-Type': 'application/json; charset=utf-8'
    # You can add more headers if necessary
}

data_PDlist = pd.DataFrame({
    "id": [],
    "name": [],
    "imageId": [],
    "videoId": [],
})

def get_media_url(data, media_type):
    try:
        return next(media['url'] for media in data['media'] if media['mediaType'] == media_type)
    except (KeyError, StopIteration):
        return None

def rm_selected_text(string, rmtext):
    """
    This function removes the specified text (rmtext) from each string in the string_list.
    
    Parameters:
    string_list (list): List of strings.
    rmtext (str): Text to be removed from the strings in string_list.
    
    Returns:
    list: A new list with the selected text removed from each string, or None if an error occurs.
    """
    try:
        # Ensure string_list is a list and rmtext is a string
        if not isinstance(rmtext, str):
            raise TypeError("The text to remove must be a string.")
        
        # Process the list and remove the specified text
        return string.replace(rmtext, '') 
    
    except Exception as e:
        # Handle errors, printing the exception or logging it as needed
        print(f"An error occurred: {e}")
        return None
    
def downloader(url):
    response = requests.get(
    url = url,
    headers=headers
    )
    return response

import subprocess
import os

def convert_video_to_audio_ffmpeg(Cname):

    """Converts video to audio directly using `ffmpeg` command
    and adds a cover image to the audio file"""

    # Define file paths
    video_path = f'{path}/{Cname}.mp4'
    image_path = f'{path}/{Cname}.jpg'
    audio_path = f'{path}/{Cname}.m4a'

    # Ensure that both the audio and image files exist
    if not os.path.isfile(video_path):
        print(f'Audio file not found: {video_path}')
        return

    if not os.path.isfile(image_path):
        print(f'Image file not found: {image_path}')
        return
    
    subprocess.call(["ffmpeg", "-i", video_path, "-vn", "-acodec", "copy", audio_path], 
                stdout=subprocess.DEVNULL, 
                stderr=subprocess.STDOUT)

    # Run the ffmpeg command to add the cover image to the audio
    subprocess.call(['neroAacTag.exe', audio_path, '-meta:artist=ibi', '-meta:track=1', '-meta:totaltracks=1',
                f'-meta:title={Cname}', '-meta:genre=piano', f'-add-cover:front:{image_path}'], 
                stdout=subprocess.DEVNULL, 
                stderr=subprocess.STDOUT)

    print(f'Audio with cover created: {audio_path}')

    os.remove(video_path)
    os.remove(image_path)


def download_combiner(Cname, CimageId, CvideoId):
    if os.path.isfile(f'{path}/{Cname}.m4a'):
        # print(f'{name}Already exists')
        return
    else:
        # print(f'Downloading{name}')
        pass

    if CimageId is not None:
        CimageIdurl = f'https://static.wixstatic.com/media/{CimageId}'
    else:
        CimageIdurl = f'https://static.wixstatic.com/media/{CvideoId}f002.jpg'

    responseImage = downloader(CimageIdurl)

    with open(f'{path}/{Cname}.jpg', 'wb') as file:
        for data in responseImage.iter_content(4096):
            file.write(data)
    
    
    for p in ['1080p', '720p', '480p', '360p']:
        CvideoIdurl = f'https://video.wixstatic.com/video/{CvideoId}/{p}/mp4/file.mp4'  # Correcting .mpa to .mp4
        responseVideo = downloader(CvideoIdurl)
        if responseVideo.status_code == 200:
            print(f'Successful download at resolution: {p}')
            break  # Break the loop once a valid video is found
        else:
            print(f'Failed at resolution: {Cname} {p}, status code: {responseVideo.status_code}')

    with open(f'{path}/{Cname}.mp4', 'wb') as file:
        for data in responseVideo.iter_content(4096):
            file.write(data)

    convert_video_to_audio_ffmpeg(Cname)


# Make the API request
response = requests.get(url, params=params, headers=headers)

# Ensure the response is successful
if response.status_code == 200:
    data = json.loads(response.text)['data']['catalog']['category']['productsWithMetaData']['list']

    with open('data.json', 'w') as json_file:
        json.dump(data, json_file, indent=4)

    data_PDlist.to_csv('data_PDlist.csv', index=False)
    # Print the filtered products
    print('success!!')
else:
    print(f"Failed to fetch data. Status code: {response.status_code}")

def is_path(path):
    if not os.path.exists(path):
        os.mkdir(path)

path = './ibipiano'
is_path(path)

data_PDlist['id'] = [data['id'] for data in data]
data_PDlist['name'] = [data['name'] for data in data]
data_PDlist['imageId'] = [get_media_url(product, 'PHOTO') for product in data]
data_PDlist['videoId'] = [get_media_url(product, 'VIDEO') for product in data]
data_PDlist['name'] = data_PDlist['name'].apply(rm_selected_text, rmtext =" (Midi File)")
data_PDlist['videoId'] = data_PDlist['videoId'].apply(rm_selected_text, rmtext ="f002.jpg")

def process_row(k, data_PDlist):

    print("Processing row: ", k)
    Cname = data_PDlist.iloc[k].get('name')
    CimageId = data_PDlist.iloc[k].get('imageId')
    CvideoId = data_PDlist.iloc[k].get('videoId')
    print("Audio name: ",Cname)
    download_combiner(Cname, CimageId, CvideoId)

    

if __name__ == '__main__':
    with ThreadPoolExecutor(max_workers=4) as executor:
        for k in range(len(data_PDlist)):
            executor.submit(process_row, k, data_PDlist)
            #if (k == 4): break
