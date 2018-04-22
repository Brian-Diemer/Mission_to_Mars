# Import Modules
import requests
from bs4 import BeautifulSoup
import pandas as pd


def scrape():

    # Get News
    url_1 = 'https://mars.nasa.gov/news/'
    response_1 = requests.get(url_1)
    soup_1 = BeautifulSoup(response_1.text, 'html.parser')
    news_title = soup_1.find('div', class_="content_title").find('a').text
    body = soup_1.find('div', class_="rollover_description_inner").text

    # Get Image URL
    url_img = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    url_root = 'https://www.jpl.nasa.gov/'
    response_soup = requests.get(url_img)
    image_soup = BeautifulSoup(response_soup.text, 'html.parser')
    image = image_soup.find('a', attrs={'id': 'full_image', 'data-fancybox-href': True}).get('data-fancybox-href')
    image_url = url_root + image
 
    # Get Tweet
    url_2 = 'https://twitter.com/marswxreport?lang=en'
    response_2 = requests.get(url_2)
    soup_2 = BeautifulSoup(response_2.text, 'html.parser')
    tweet = soup_2.find('div', class_='js-tweet-text-container').find('p').text

    # Get Table
    table_url = 'http://space-facts.com/mars/'
    tables = pd.read_html(table_url)
    mars_df = tables[0]
    mars_df.columns = ['Description','Value']
    mars_df.set_index('Description', inplace=True)
    mars_table = mars_df.to_dict()

    # Hemispheres dictionaries
    cer_link = 'https://astrogeology.usgs.gov/search/map/Mars/Viking/cerberus_enhanced'
    sch_link = 'https://astrogeology.usgs.gov/search/map/Mars/Viking/schiaparelli_enhanced'
    syr_link = 'https://astrogeology.usgs.gov/search/map/Mars/Viking/syrtis_major_enhanced'
    val_link = 'https://astrogeology.usgs.gov/search/map/Mars/Viking/valles_marineris_enhanced'

    mars_hem = [cer_link, sch_link, syr_link, val_link]

    cer_dict = {}
    cer_html = requests.get(cer_link)
    soup_cer = BeautifulSoup(cer_html.text, 'html.parser')
    title = soup_cer.find('h2', class_='title').text
    cer_url = soup_cer.find('div', class_='downloads')
    cer_url = cer_url.a['href']
    cer_dict['title'] = title
    cer_dict['link'] = cer_url
 
    sch_dict = {}
    sch_html = requests.get(sch_link)
    soup_sch = BeautifulSoup(sch_html.text, 'html.parser')
    title = soup_sch.find('h2', class_='title').text
    sch_url = soup_sch.find('div', class_='downloads')
    sch_url = sch_url.a['href']
    sch_dict['title'] = title
    sch_dict['link'] = sch_url

    syr_dict = {}
    syr_html = requests.get(syr_link)
    soup_syr = BeautifulSoup(syr_html.text, 'html.parser')
    title = soup_syr.find('h2', class_='title').text
    syr_url = soup_syr.find('div', class_='downloads')
    syr_url = syr_url.a['href']
    syr_dict['title'] = title
    syr_dict['link'] = syr_url

    val_dict = {}
    val_html = requests.get(val_link)
    soup_val = BeautifulSoup(val_html.text, 'html.parser')
    title = soup_val.find('h2', class_='title').text
    val_url = soup_val.find('div', class_='downloads')
    val_url = val_url.a['href']
    val_dict['title'] = title
    val_dict['link'] = val_url

    hem_list = [cer_dict, sch_dict, syr_dict, val_dict]
    hem_list

    # Create Dictionary with everything
    mars_dict = {}
    mars_dict = {'news_title': news_title, 'news_text': body,
                 'featured_image': image_url, 'Tweet': tweet,
                 'facts': mars_table, 'hemisphere_images': hem_list}
    return mars_dict