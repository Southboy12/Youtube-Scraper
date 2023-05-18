from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import pandas as pd
import smtplib
import os

YOUTUBE_TRENDING_URL = 'https://www.youtube.com/feed/trending'

def get_driver():
  chrome_options = Options()
  chrome_options.add_argument('--no-sandbox')
  chrome_options.add_argument('--headless')
  chrome_options.add_argument('--disable-dev-shm-usage')
  driver = webdriver.Chrome(options=chrome_options)
  return driver

def load_all_pages(driver):
  WAIT_IN_SECONDS = 5
  last_height = driver.execute_script("return document.documentElement.scrollHeight")
  
  while True:
      # Scroll to the bottom of page
      driver.execute_script("window.scrollTo(0, arguments[0]);", last_height)
      # Wait for new videos to show up
      time.sleep(WAIT_IN_SECONDS)
      
      # Calculate new document height and compare it with last height
      new_height = driver.execute_script("return document.documentElement.scrollHeight")
      if new_height == last_height:
          break
      last_height = new_height

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
  videos_df = pd.DataFrame(videos)
  print(videos_df.shape)
  if videos_df.shape[0] > 90:
    videos_df.to_csv('Trending.csv', index=None)
  else:
    get_video(driver)   

def send_email():
  
  try:
    server_ssl = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server_ssl.ehlo()

    SENDER_EMAIL = 'rapidapitest10@gmail.com'
    RECEIVER_EMAIL = 'rapidapitest10@gmail.com' 
    SENDER_PASSWORD = os.environ['GMAIL_PASSWORD']
  
    subject = 'Test message from Replit'
    body = 'Hey, this is a test from Replit  (live workshop)'
  
    email_text = f"""
    From: {SENDER_EMAIL}
    To: {RECEIVER_EMAIL}
    Subject: {subject}
    
    {body}
    """

    server_ssl.login(SENDER_EMAIL, SENDER_PASSWORD)
    server_ssl.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, email_text)
    server_ssl.close()
    
  except:
    print('Something went wrong...')

def parent_func():
  print('==== Getting Browser ====')\n
  driver = get_driver()
  print('==== Browser Ready ====')\n
  print('==== Load all the videos ====')\n
  load_all_pages(driver)
  print('==== All videos loaded ====')\n
  print('==== scraping data ====') \n
  get_video(driver)
  print('==== Successfully scraped and converted to csv ====')\n
  print("==== Send an email ====")
  send_email()
  

if __name__ == '__main__':
  parent_func()