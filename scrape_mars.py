
# coding: utf-8

# # Mission to Mars

# ## Step 1 - Scraping

# Dependencies
import pandas as pd
import requests

import time
from splinter import Browser
from bs4 import BeautifulSoup
from selenium import webdriver

import tweepy
import TweepyCredentials # twitter keys and tokens
import pymongo

# Setting up splinter
def init_browser():
    executable_path = {"executable_path": "chromedriver"}
    return Browser("chrome", **executable_path, headless=False)

# Define a function 
def scrape():
    browser = init_browser()
    # create mars_data dict that we can insert into mongo
    mars_data = {}

    #############################################
    
    # ### NASA Mars News 

    # URL of NASA Mars News to be scraped for latest news and paragraph title
    url_NASA_Mars_News = 'https://mars.nasa.gov/news/'
    browser.visit(url_NASA_Mars_News)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')


    # Latest News Title from NASA Mars News Site
    print("Test 1")
    news_title = soup.find_all('div', class_='content_title')
    print(news_title[0].text)
    print("Test 2")

    # Latest News Paragraph Text from NASA Mars News Site
    news_p = soup.find_all('div', class_='article_teaser_body')
    print(news_p[0].text)
    print("Test 3")

    # # Adding latest news and paragraph title to the dictionary
    mars_data['news_title'] = news_title[0].text
    mars_data['news_p'] = news_p[0].text
    print("Test 4")



    ############################################

    # ### JPL Mars Space Images - Featured Image

    # URL of JPL Mars Space Image to be scraped for featured image
    url_JPL_images = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url_JPL_images)
    print("Test 5")


    # Browse through the pages
    time.sleep(5)

    # Click the full image button
    browser.click_link_by_partial_text('FULL IMAGE')
    time.sleep(5)
    print("Test 6")


    # Click the more info button
    browser.click_link_by_partial_text('more info')
    time.sleep(5)
    print("Test 7")


    # Using BeautifulSoup create an object and parse with 'html.parser'
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    print("Test 8")


    # Get featured image
    result = soup.find('article')
    image_path = result.find('figure','lede').a['href']
    JPL_link = 'https://www.jpl.nasa.gov'
    featured_image_url = JPL_link + image_path
    featured_image_url
    print("Test 9")

    # Adding featured image url to the dictionary
    mars_data['featured_image_url'] = featured_image_url
    print("Test 10")

    #############################################

    # ### Mars Weather

    # Twitter API Keys
    consumer_key = TweepyCredentials.consumer_key
    consumer_secret = TweepyCredentials.consumer_secret
    access_token = TweepyCredentials.access_token
    access_token_secret = TweepyCredentials.access_token_secret


    # Setup Tweepy API Authentication
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth, parser=tweepy.parsers.JSONParser())


    # Target User
    target_user = "@MarsWxReport"


    # Retrive latest tweet
    tweet = api.user_timeline(target_user)
    mars_weather = tweet[0]['text']
    mars_weather

    # Adding mars weather from the latest rweet  to the dictionary
    mars_data['mars_weather'] = mars_weather

    #############################################

    # ### Mars Facts

    # URL of Mars facts to scrape the table containing facts about the planet
    # url_Mars_Facts = 'https://space-facts.com/mars/'
    # browser.visit(url_Mars_Facts)
    # print("Test 11")


    # html = browser.html
    # soup = BeautifulSoup(html, 'html.parser')
    # print("Test 12")


    # # Create empty lists for storing Mars info
    # description = []
    # value = []

    # # Scrape the info from URL
    # results = soup.find('tbody').find_all('tr')
    # print("Test 13")

    # # Store all the information in dictionary
    # for result in results:
    #     elements = result.find_all('td')
    #     description.append(elements[0].text)
    #     value.append(elements[1].text)
    
    # # Create a dataframe from this dictionary
    # mars_profile_df = pd.DataFrame({"Description": description, "Value": value})
    # print("Test 14")

    # # Visualize the dataframe
    # mars_profile_df


    # # Convert the dataframe to HTML table string
    # mars_profile_html = mars_profile_df.to_html()
    # mars_profile_html
    # print("Test 15")

    # Adding mars facts to the dictionary
    # mars_data['mars_profile_df'] = mars_profile_df

    ############################################

    # ### Mars Hemisphere

    # # Scapping of  USGS Astrogeology site to obtain high resolution images for each of Mars hemispheres.
    # url_USGS = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

    # # Setting up splinter
    # executable_path = {'executable_path': 'chromedriver'}
    # browser = Browser('chrome', **executable_path)
    # browser.visit(url_USGS)

    # html = browser.html
    # soup = BeautifulSoup(html, 'html.parser')


    # # Create an empty list to hold dictionaries of hemisphere title with the image url string
    # hemisphere_image_urls = []

    # # Get the class holding all images of hemisphere
    print(mars_data)
    print("hi!!")
    return mars_data
