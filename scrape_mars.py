from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
import requests
import pandas as pd


def init_browser():

    executable_path = {"executable_path": "chromedriver"}
    return Browser("chrome", **executable_path, headless=False)


def scrape():
    browser = init_browser()
    mars_data = {}
#----------------------------------------------------------------------
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)

    html = browser.html
    soup = bs(html, "html.parser")

    news = soup.find('div', id='page')
    news_title = news.find_all('a')[1].text
    news_pra = news.find_all('a')[0].text

    mars_data["news_title"] = news_title
    mars_data["news_p"] = news_pra
#----------------------------------------------------------------------
    base_url = "https://www.jpl.nasa.gov"
    img_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(img_url)
    time.sleep(1)

    html = browser.html
    soup = bs(html, "html.parser")

    featured_img = soup.find("div", class_="carousel_items").find("article")["style"]
    featured_img = featured_img.split("'")[1]
    featured_img_url = base_url + featured_img
    mars_data["featured_img_url"] = featured_img_url
    print(featured_img_url)

#----------------------------------------------------------------------
    twitter_url= "https://twitter.com/marswxreport?lang=en"
    response = requests.get(twitter_url)
    soup = bs(response.text, 'html.parser')
    mars_weather= soup.find(class_="TweetTextSize").text.strip()
    mars_data["mars_weather"] = mars_weather
    print(mars_weather)
#----------------------------------------------------------------------
    facts_url = 'https://space-facts.com/mars/'
    tables = pd.read_html(facts_url)
    df = tables[0]
    df.set_index('Mars - Earth Comparison', inplace=True)
    
    html_table = df.to_html()
    html_table = html_table.replace('\n', '')

    mars_data["mars_facts"] = html_table
    print(html_table)
#----------------------------------------------------------------------
    html = browser.html
    soup = bs(html, "html.parser")
    
    hem_base="https://astrogeology.usgs.gov"
    hemmain= "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    
    response= requests.get(hemmain)
    soup = bs(response.text, 'html.parser')
    
    imgtitles=[]
    for x in soup.find_all(class_='item'):
        title= x.find('h3').text.strip()
        imgtitles.append(title)
    
    link_list = [a['href'] for a in soup.find_all('a', class_="itemLink product-item", href=True)]
    
    fulllinklist= []
    for x in link_list:
        fulllink= hem_base + x
        fulllinklist.append(fulllink)

    hemimagelist=[]
    for x in fulllinklist:
        url = x
        response=requests.get(url)
        soup= bs(response.text, 'html.parser')
        img_link_list = soup.find('a', target="_blank" ,href=True)
        hemimage= img_link_list['href']
        hemimagelist.append(hemimage)

    hemisphere_image_url = []

    for x in range(len(imgtitles)):
        title= imgtitles[x]
        image_url= hemimagelist[x]
        hemisphere_image_url.append({"title":title,"img_url":image_url})
    mars_data['hemisphere_image_url']= hemisphere_image_url
    mars_data['first_title']= hemisphere_image_url[0]["title"]
    mars_data['second_title']= hemisphere_image_url[1]["title"]
    mars_data['third_title']= hemisphere_image_url[2]["title"]
    mars_data['fourth_title']= hemisphere_image_url[3]["title"]

    mars_data['first_img']= hemisphere_image_url[0]["img_url"]
    mars_data['second_img']= hemisphere_image_url[1]["img_url"]
    mars_data['third_img']= hemisphere_image_url[2]["img_url"]
    mars_data['fourth_img']= hemisphere_image_url[3]["img_url"]

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
    # print(hemisphere_image_urls)
    return mars_data
