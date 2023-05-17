from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from pprint import pprint

YOUTUBE_TRENDING_URL = 'https://www.youtube.com/feed/trending'

def get_driver():
  chrome_options = Options()
  chrome_options.add_argument('--no-sandbox')
  chrome_options.add_argument('--headless')
  chrome_options.add_argument('--disable-dev-shm-usage')
  driver = webdriver.Chrome(options=chrome_options)
  return driver


def get_video(driver):
  driver.get(YOUTUBE_TRENDING_URL)
  page_title = driver.title
  #print(page_title)
  title_tags = driver.find_elements(By.XPATH, '//a[@id="video-title"]')
  titles = [title_tag.text for title_tag in title_tags]
  #print(titles)
  links = [title_tag.get_attribute('href') for title_tag in title_tags]
  #print(links)
  #driver.find_elements(By.TAG_NAME, 'ytd-video-renderer')
  thumbnail_tags = driver.find_elements(By.XPATH, '//a[@id="thumbnail"]/yt-image/img')
  thumbnails = [thumbnail_tag.get_attribute('src') for thumbnail_tag in thumbnail_tags]
  #print(thumbnails)
  description_tags = driver.find_elements(By.XPATH, '//yt-formatted-string[@id="description-text"]')
  descriptions = [description_tag.text for description_tag in description_tags]
  #print(descriptions)
  view_tags = driver.find_elements(By.XPATH, '//div[@id="metadata-line"]/span[1]')
  views = [view_tag.text for view_tag in view_tags]
  #print(views)
  uploaded_time_tags = driver.find_elements(By.XPATH, '//div[@id="metadata-line"]/span[2]')
  uploaded_times = [uploaded_time_tag.text for uploaded_time_tag in uploaded_time_tags]
  #print(uploaded_times)
  channel_tags = driver.find_elements(By.XPATH, '//yt-formatted-string[@id="text"]/a')
  channels = [channel_tag.text for channel_tag in channel_tags]
  #print(channels)
  channel_urls = [channel_tag.get_attribute('href') for channel_tag in channel_tags]
  #print(channel_urls)
  videos = []
  for title, link, thumbnail, description, view, uploaded_time, channel, channel_url in zip(titles, links, thumbnails, descriptions, views, uploaded_times, channels, channel_urls):
    video_dict = {
      'title': title,
      'link' : link,
      'thumbnail' : thumbnail,
      'description' : description,
      'view': view,
      'uploadedd_time' : uploaded_time,
      'channel' : channel,
      'channel_url' : channel_url
    }
    videos.append(video_dict)
  pprint(videos)

if __name__ == '__main__':
  driver = get_driver()
  get_video(driver)