#web scrape the beginning

import bs4
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup

theurl = 'https://www.newegg.com/Video-Cards-Video-Devices/Category/ID-38?Tpk=graphics%20cards'

#open up connection and download the page
uClient = uReq(theurl)
page_raw = uClient.read()
uClient.close()

#html parser
page_soup = soup(page_raw, "html.parser")
#grabs each item
the_containers = page_soup.findAll("div",{"class":"item-container"})
container = the_containers[0]

#print(container.find('a',"item-brand"))
#spec_brand = container.find("li","price-ship").text.strip()
#print(spec_brand)

#write a cvs file to the pytest directory
filename = "gc_products.csv"
f = open(filename, "w")
headers = "brand, product_name, shipping_cost\n"
f.write(headers)

for container in the_containers:
    spec_brand = container.find("div", "item-branding").a.img["title"]
    spec_title = container.a.img["title"]
    shipping_cost = container.find("li","price-ship").text.strip()

    print("brand: " + spec_brand)
    print("product_name: " + spec_title)
    print("shipping_cost: " + shipping_cost)
    f.write(spec_brand + "," + spec_title.replace(",","|") + ","+ shipping_cost+"\n")

f.close()
