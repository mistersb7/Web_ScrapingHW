from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
import requests
import pandas as pd


def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "chromedriver.exe"}
    return Browser("chrome", ** executable_path, headless=False)


def scrape():
    browser = init_browser()

    url = "https://mars.nasa.gov/news/"
    response = requests.get(url1)
    browser.visit(url)

    html = browser.html
    soup = bs(html, "html.parser")

    # -------------------------------------------------
    # Title & Paragraph
    news_title = soup.find(class_="content_title").text.strip()
    news_p= soup.find(class_="rollover_description_inner").text.strip()
    

    # -------------------------------------------------
    # FEATURED IMAGE
    
    url2= "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    response2 = requests.get(url2)
    base_url= "https://www.jpl.nasa.gov"
    soup2 = bs(response2.text, 'html.parser')
    featured_img = soup2.find("div", class_="carousel_items").find("article")["style"]
    featured_img = featured_img.split("'")[1]
    img_url= base_url + featured_img
    


    #-------------------------------------------------
    # TWITTER FEED
    twitter_url= "https://twitter.com/marswxreport?lang=en"
    response3 = requests.get(twitter_url)
    soup = bs(response3.text, 'html.parser')
    mars_weather= soup.find(class_="TweetTextSize").text.strip()
    #mars_data["mars_weather"] = mars_weather

    mars_data = {
        "news_title": news_title,
        "news_p": news_p,
        "img_url": img_url,
        "mars_data": mars_weather
    }
    browser.quit()
    #-------------------------------------------------
    #
    # facts_url = 'https://space-facts.com/mars/'
    # tables = pd.read_html(facts_url)
    # df = tables[0]
    # df.set_index('Mars - Earth Comparison', inplace=True)
    
    # html_table = df.to_html()
    # html_table = html_table.replace('\n', '')

    # mars_data["mars_facts"] = html_table

    #-------------------------------------------------


    # hemisphere_image_urls = []
    # hem_url="https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    # response= requests.get(hem_url)
    # soup = bs(response.text, 'html.parser')
    # for x in soup.find_all(class_='item'):
    #     title= x.find('h3').text.strip()
    #     image = x.find('img')
    #     image_url= image['src']
    #     hemisphere_image_urls.append({"title":title,"img_url":image_url})
    # mars_data["mars_hemisphere"] = hemisphere_image_urls

    return mars_data
