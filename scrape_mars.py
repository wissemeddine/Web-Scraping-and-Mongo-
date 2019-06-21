    
#import dependencies
from bs4 import BeautifulSoup as bs
from splinter import Browser
import os
import pandas as pd
import time
import requests
from selenium import webdriver


def init_browser():
    executable_path = {'executable_path': 'chromedriver.exe'}
    return Browser("chrome", **executable_path, headless = False)

# create a dictionary that import into mongo 
mars_data_info = {}
# collecting the Nasa Mars News
def scrape_mars_news():
    try: 

        # calling browser 
        browser = init_browser()
        # using splinter module to visit the nasa url 
        news_url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
        browser.visit(news_url)
        # HTML Object
        html = browser.html
        # Parse HTML with BeautifulSoup
        soup = bs(html, 'html.parser')
        # collecting the latest data that contains news title and news paragraph
        news_title = soup.find('div', class_='content_title').find('a').text
        news_paragraph = soup.find('div', class_='article_teaser_body').text
        # filling up dictionary with nasa news. 
        mars_data_info['news_title'] = news_title
        mars_data_info['news_paragraph'] = news_paragraph

        return mars_data_info

    finally:

        browser.quit()

# Mars image ///////////////////////////////
def scrape_mars_image():
    try: 
        # calling browser 
        browser = init_browser()
        # Visit Mars Space Images through splinter module
        featured_image_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
        browser.visit(featured_image_url)
        # HTML Object 
        html_image = browser.html
        # Parse HTML with Beautiful Soup
        soup = bs(html_image, 'html.parser')
        # Retrieve background-image url from style tag 
        featured_image_url  = soup.find('article')['style'].replace('background-image: url(','').replace(');', '')[1:-1]
        # Website Url 
        base_url = 'https://www.jpl.nasa.gov'
        # Concatenate website url with scrapped route
        featured_image_url = base_url + featured_image_url
        # Display full link to featured image
        featured_image_url 
        # Dictionary entry from FEATURED IMAGE
        mars_data_info['featured_image_url'] = featured_image_url 
        return mars_data_info
    finally:

        browser.quit()       

# Mars Weather
 
def scrape_mars_weather():

    try: 
        # calling browser 
        browser = init_browser()

        #browser.is_element_present_by_css("div", wait_time=1)

        # Visit Mars Weather Twitter through splinter module
        mars_weather_url = 'https://twitter.com/marswxreport?lang=en'
        browser.visit(mars_weather_url)

        # HTML Object 
        html_mars_weather = browser.html

        # Parse HTML with BeautifulSoup
        soup = bs(html_mars_weather, 'html.parser')

        # search for data that contain tweets
        latest_weather_tweets = soup.find("p", class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text
        mars_data_info['latest_weather_tweets'] = latest_weather_tweets
        
        return mars_data_info
    finally:

        browser.quit()


# Mars Facts
def scrape_mars_facts():

    # Visit Mars facts url 
    url_mars_facts = 'http://space-facts.com/mars/'

    # Use Panda's `read_html` to parse the url
    mars_facts = pd.read_html(url_mars_facts)

    # Find the mars facts DataFrame in the list of DataFrames as assign it to `mars_df`
    df_mars_facts = mars_facts [0]

    # Assign the columns `['Description', 'Value']`
    df_mars_facts.columns = ['Description','Values']

    # Set the index to the `Description` column without row indexing
    df_mars_facts.set_index('Description', inplace=True)

    # Save html code to folder Assets
    data = df_mars_facts.to_html()

    # Dictionary entry from MARS FACTS
    mars_data_info['mars_facts'] = data

    return mars_data_info


# MARS HEMISPHERES


def scrape_mars_hemispheres():

    try: 
        # Initialize browser 
        browser = init_browser()
        # Visit hemispheres website through splinter module 
        hemispheres_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
        browser.visit(hemispheres_url)
        # HTML Object
        html_hemispheres = browser.html
        # Parsing HTML using Beautiful Soup
        soup = bs(html_hemispheres, 'html.parser')
        # calling data items that contain mars hemispheres
        items = soup.find_all('div', class_='item')
        # Create empty list for hemisphere image urls 
        hemispheres_images_url= []
        # Store the main_ul 
        hemispheres_main_url = 'https://astrogeology.usgs.gov' 
        # Looping through the items previously saved
        for i in items: 
            # Store title
            title = i.find('h3').text
            # Store image website link and visit the website
            stored_img_url = i.find('a', class_='itemLink product-item')['href']
            browser.visit(hemispheres_main_url + stored_img_url)
            # HTML Object of individual hemisphere information website 
            stored_img_html = browser.html
            # Parse HTML with BeautifulSoup for every individual hemisphere information website 
            soup = bs( stored_img_html, 'html.parser')
            # calling  full image source 
            full_img_url = hemispheres_main_url + soup.find('img', class_='wide-image')['src']
            # Append the retreived information into a list of dictionaries 
            hemispheres_images_url.append({"title" : title, "img_url" : full_img_url})

        mars_data_info['hemispheres_images_url'] = hemispheres_images_url

        
        # Return mars_data dictionary 

        return mars_data_info
    finally:

        browser.quit()
