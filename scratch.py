import requests
from bs4 import BeautifulSoup as bs


YOUTUBE_TRENDING_URL = 'https://www.youtube.com/feed/trending'

response = requests.get(YOUTUBE_TRENDING_URL)

print('Status Code', response.status_code)

with open('trending.html', 'w') as f:
  f.write(response.text)

doc = bs(response.text, 'html.parser')

print('Page title', doc.title)

video_divs = doc.find_all('div', class_='style-scope ytd-video-renderer')

print(f'Found {len(video_divs)} videos')