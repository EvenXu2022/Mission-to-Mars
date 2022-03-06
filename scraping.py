#!/usr/bin/env python
# coding: utf-8
# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager
import datetime as dt

def scrape_all():
    # Initiate headless driver for deployment
    executable_path = {'executable_path': "ChromeDriver.exe"}
    browser = Browser('chrome', **executable_path, headless=True)

    news_title, news_paragraph = mars_news(browser)

    # Run all scraping functions and store results in a dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "last_modified": dt.datetime.now(),
        "hemispheres":hemisphere(browser)
    }

    # Stop webdriver and return data
    browser.quit()
    return data

def mars_news(browser):
    url = 'https:/redplanetscience.com'
    browser.visit(url)
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    html = browser.html
    news_soup = soup(html, 'html.parser')
    try: 
        slide_elem = news_soup.select_one('div.list_text')
        
        news_title = slide_elem.find('div', class_='content_title').get_text()
        
        # Use the parent element to find the paragraph text
        news_paragraph = slide_elem.find('div', class_='article_teaser_body').get_text()
    except AttributeError:
        return None, None

    return news_title, news_paragraph

# ### Featured Images
def featured_image(browser):
    url = 'https://spaceimages-mars.com'
    browser.visit(url)

    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    html = browser.html
    img_soup = soup(html, 'html.parser')
    try: 
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')

    except AttributeError:
        return None
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'

    return img_url

def mars_facts():
    # Add try/except for error handling
    try:
        # Use 'read_html' to scrape the facts table into a dataframe
        df = pd.read_html('https://galaxyfacts-mars.com')[0]

    except BaseException:
        return None

    # Assign columns and set index of dataframe
    df.columns=['Description', 'Mars', 'Earth']
    df.set_index('Description', inplace=True)

    # Convert dataframe into HTML format, add bootstrap
    return df.to_html()

def hemisphere(browser):

    url = 'https://marshemispheres.com/'
    browser.visit(url)
    hemisphere_image_urls = []

    for i in range(4):
        #create empty dictionary
        
        hemispheres = {}
        #find elements going to click link
        browser.find_by_css('h3')[i].click()
        # define html
        html = browser.html
        img_soup = soup(html, 'html.parser')
        # fine 'sample' image link
        img_url = browser.find_by_text('Sample').first['href']
    #     img_url2_rel= img_soup.find('div',id="wide-image").find('a', target="_blank").get('href')
    #     img_url2 = f"{url}{img_url2_rel}"
        
        # find image title
        title = browser.find_by_tag('h2.title').text

        # adding data into hemispheres dictionary
        hemispheres["img_url"] = img_url
        hemispheres["title"] = title
        hemisphere_image_urls.append(hemispheres)
        
        # browser go back
        browser.back()
    return hemisphere_image_urls


if __name__ == "__main__":
    print(scrape_all())
