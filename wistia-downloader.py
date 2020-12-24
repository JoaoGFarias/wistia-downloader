import urllib.request
import re
import requests
import sys
import uuid

def fetch_html(code):
    target_url = f"https://fast.wistia.net/embed/iframe/{code}"
    return ''.join([line.decode('utf-8') for line in urllib.request.urlopen(target_url)])

def find_binary_urls(html):
    return ['https://embed-ssl.wistia.com/deliveries/'+id+'.mp4' for id in find_binary_urls_ids(html)]

def find_binary_urls_ids(html):
    return re.findall(r'https://embed-ssl.wistia.com/deliveries/(.*?).bin', html)

def download_file(urls, filename = "test"):
    try:
        request = requests.get(urls[0])
        complete_filename = f'{filename}.mp4'
        with open(complete_filename, 'wb') as f:
            f.write(request.content)
        
        print(f'Download the file of code {code} completed. Name: {complete_filename}')
    except IndexError:
        print(f'Downloading the file failed')

def download_file_of_code(code, filename):
    print(f'Preparing to download the file of code {code}')
    html = fetch_html(code)
    urls = find_binary_urls(html)
    download_file(urls, filename)


if __name__ == "__main__":
    sys.argv.pop(0)
    prefix = sys.argv.pop(0)
    execution_id = str(uuid.uuid4())
    print(f'Execution ID: {execution_id}')

    for index, code in enumerate(sys.argv):
        download_file_of_code(code, f'{prefix}-{execution_id}-{index}')
