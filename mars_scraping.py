from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
import pandas as pd

def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)

def mars_news():
	mars_data={}
	browser = init_browser()
    #1. NASA Mars News scrape
	url = 'https://mars.nasa.gov/news/'
	print("Visiting news page")
	browser.visit(url)

	# Scrape page into Soup
	html = browser.html
	print("Scraping data...")
	soup = bs(html, 'html.parser')
	# latest article title 
	news_title = soup.find('div', class_='content_title').find('a').text
	print("Found title..")
	# latest article paragraph 
	news_p = soup.find('div', class_='article_teaser_body').text
	mars_data['news_title'] = news_title
	mars_data['news_p'] = news_p
	print("Quitting browser")
	browser.quit()
	return mars_data

	#2.scrape freatured image on nasa.gov

def featured_img():
	mars_data={}
	img_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
	browser = init_browser() 
	browser.visit(img_url)

	html = browser.html

	# Scrape page into Soup
	soup = bs(html, "html.parser")

	# Featured image on mars 
	# Return results
	articles=soup.find('div',class_="carousel_items").find('article')
	imgtag=articles['style']

	base_path='https://www.jpl.nasa.gov/'
	#extract url from style
	#get image URL through a string split
	rel_path=imgtag.split("('", 1)[1].split("')")[0]
	featured_image = base_path+ rel_path
	mars_data['featured_image'] = featured_image
	browser.quit()
	return mars_data

	
	#3.scrape Mars weather

def mars_weather():
	mars_data={}
	browser = init_browser() 

	weather_url = "https://twitter.com/marswxreport?lang=en"
	browser.visit(weather_url)
	html = browser.html
	soup = bs(html, "html.parser")
	weather_rel_path = soup.find("div", class_= "js-tweet-text-container")
	mars_weather=weather_rel_path.find(class_="tweet-text")

	myweather=''
	i=0
	for tag in mars_weather:
		i=i+1
		if i==1:
			myweather=tag.string
			print(myweather)
	mars_data['weather'] = myweather
	browser.quit()
	return mars_data



	#4. scrape mars facts

def mars_facts():
	mars_data={}
	browser = init_browser()
	
	# scrape mars facts table
	marsFacts_url = "https://space-facts.com/mars/"
	browser.visit(marsFacts_url)
	html = browser.html
	soup = bs(html, "html.parser")

	#Find Table and turn into data frame
	marsFacts_table = soup.find("table",class_="tablepress-id-mars")
	table_rows = marsFacts_table.find_all('tr')

	res = []
	for tr in table_rows:
	    td = tr.find_all('td')
	    row = [tr.text.strip() for tr in td if tr.text.strip()]
	    if row:
	        res.append(row)

	#Initialize the pandas data frame
	df = pd.DataFrame(res,columns=['Description','Measurement'])
	

	mars_data['facts'] = res

	browser.quit()
	return mars_data


	# 5. scrape mars hemisphere

def get_link_image(browser,link):
    browser.visit(link)
    html=browser.html
    sp=bs(html,"html.parser")
    tags=sp.find("div",class_="downloads").find('ul').find('li').find('a')
    imglink=tags['href']
    if 'jpg' in imglink:
        return(imglink)
    else:
        return(None)



def mars_hemis():
	mars_data={}
	browser = init_browser()

	marsurl='https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
	browser.visit(marsurl)
	html=browser.html

	#Find all the items
	soup = bs(html, "html.parser")
	#Find all links('a') on the page
	items= soup.find_all("a",class_="itemLink product-item")

	marsroot='https://astrogeology.usgs.gov'

	i=0
	hemisphere_image_urls=[]
	for tag in items:
	    imageURL=marsroot+tag['href']
	    title=tag.find('h3')
	    if title is not None:
	        i=i+1
	        print(imageURL)
	        name=title.string
	        print(name)
	        print("Title is "+title.string)
	        #Call the function to follow the links
	        fullimglink=get_link_image(browser,imageURL)
	        if fullimglink is not None:
	            hemisphere_image_urls.append({"title" : name, 'img_url':fullimglink })

	        print("----<>-----")

	#Print result dictionary
	print(hemisphere_image_urls)

	mars_data['hemisphere_image_urls'] = hemisphere_image_urls

	browser.quit()
	return mars_data

def main_mars_scrape_info():
 	news_result=mars_news()
 	print("--Lookinf for Images")
 	image_result=featured_img()
 	print("--Looking  for mars weather")
 	weather= mars_weather()
 	print('-- Looking for facts on mars')
 	facts = mars_facts()
 	print('--- Looking for Mars Hemis')
 	hemisphere = mars_hemis()

 	marsdata={}
 	marsdata['news']=news_result
 	marsdata['featured_image']=image_result
 	marsdata['weather']=weather
 	marsdata['hemisphere']=hemisphere
 	marsdata['facts']=facts

 	return(marsdata)











	





	









