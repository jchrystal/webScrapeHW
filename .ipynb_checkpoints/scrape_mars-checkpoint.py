from splinter import Browser
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

def init_browser():
    executable_path = {"executable_path": "./chromedriver"}
    return Browser("chrome", **executable_path, headless=False)

def scrape():
    
    browser = init_browser()
    url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"

    # Get response and create the BS object
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')

    # Store the first title and teaser text in variables
    news_title = soup.find_all('div', class_='content_title')[0].text.strip()
    news_p = soup.find_all('div', class_="rollover_description_inner")[0].text.strip()

    # Print variables to double check
    print(news_title)
    print(news_p)

    # Build the browser object using splinter to navigate chrome and pass nasa url
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)
    time.sleep(3)

    # Click thru using splinter until arrival at large image url
    browser.click_link_by_partial_text('FULL IMAGE')
    time.sleep(3)
    browser.click_link_by_partial_text('more info')
    time.sleep(3)
    browser.click_link_by_partial_href('/spaceimages/images')

    # Create another beautiful soup object with the splinter html
    soup2 = BeautifulSoup(browser.html, 'lxml')

    # Store the url into variable
    featured_img_url = soup2.find_all('img')[0]['src']
    featured_img_url

    # create bs object for mars weather twitter account
    url = "https://twitter.com/marswxreport?lang=en"
    response = requests.get(url)
    soup3 = BeautifulSoup(response.text, 'lxml')

    # Store latest tweet in variable
    mars_weather = soup3.find_all('p', class_='TweetTextSize')[0].text.strip()
    mars_weather

    # scrape mars facts HTML table and read into pandas
    url = 'https://space-facts.com/mars/'
    df_list = pd.read_html(url)
    mars_df = df_list[0]
    mars_html_table = mars_df.to_html()
    mars_html_table

    # Build browser object using splinter and pass US astrogeology url
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)

    # Create another beautiful soup object with the splinter html
    soup4 = BeautifulSoup(browser.html, 'lxml')

    # Create list of hrefs
    href_list = []

    div_list = soup4.find_all('div', class_='description')

    for div in div_list:
        href_list.append(div.a['href'])

    href_list

    # Loop through each href, use splinter to click by href and grab the img_url and title
    hemisphere_img_urls = []

    for href in href_list:
        browser.find_link_by_href(href)[1].click()
        soup4 = BeautifulSoup(browser.html, 'lxml')
        src = soup4.find_all('img', class_='wide-image')[0]['src']
        img_url = 'https://astrogeology.usgs.gov' + src
        title = soup4.find_all('h2', class_='title')[0].text.strip()
        dict_ = {'title': title, 'img_url': img_url}
        hemisphere_img_urls.append(dict_)
        browser.back()

    browser.quit()
    hemisphere_img_urls

    # Create mars dict of all above scrapes
    mars_dict = {"newsTitle": news_title,
                 "newsParagraph": news_p,
                 "featuredImage": featured_img_url,
                 "marsWeather": mars_weather,
                 "marsData": mars_html_table,
                 "marsHemispheres": hemisphere_img_urls}
    
    print(mars_dict)
    
    return mars_dict


