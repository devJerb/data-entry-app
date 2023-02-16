from bs4 import BeautifulSoup
import requests
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys

google_form = "google-form-link"
zillow_url = "https://www.zillow.com/homes/for_rent/1-_beds/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C" \
             "%22usersSearchTerm%22%3Anull%2C%22mapBounds%22%3A%7B%22west%22%3A-122.56276167822266%2C%22east%22%3A" \
             "-122.30389632177734%2C%22south%22%3A37.69261345230467%2C%22north%22%3A37.857877098316834%7D%2C" \
             "%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22fsba%22%3A" \
             "%7B%22value%22%3Afalse%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse" \
             "%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22fore%22%3A%7B" \
             "%22value%22%3Afalse%7D%2C%22pmf%22%3A%7B%22value%22%3Afalse%7D%2C%22pf%22%3A%7B%22value%22%3Afalse%7D" \
             "%2C%22mp%22%3A%7B%22max%22%3A3000%7D%2C%22price%22%3A%7B%22max%22%3A872627%7D%2C%22beds%22%3A%7B%22min" \
             "%22%3A1%7D%7D%2C%22isListVisible%22%3Atrue%2C%22mapZoom%22%3A12%7D"

# http://myhttpheader.com/
header = {
    "User-Agent": "user-agent",
    "Accept-Language": "language"
}

# web scraping
rental_listings = requests.get(url=zillow_url, headers=header).text
content = BeautifulSoup(rental_listings, 'html.parser')

# select classes
data_pane = content.find(name="div", id="search-page-list-container")
data_prices = data_pane.find_all(name="div", class_="StyledPropertyCardDataArea-c11n-8-84-2__sc-yipmu-0")
data_list_links = content.find_all(name="a", class_="property-card-link")
data_addresses = content.find_all(name="address")

# get prices
prices = []
for datum in data_prices:
    datum_price = datum.find(name="span")
    if datum_price is not None:
        prices.append(datum_price.getText())

# get addresses
addresses = []
for address in data_addresses:
    addresses.append(address.getText())

# get listing links
listing_links = []
for link in data_list_links:
    list_link = link.get("href")
    if "https://www.zillow.com" not in list_link:
        list_link = f"https://www.zillow.com{list_link}"
    listing_links.append(list_link)

# web driver
chrome_driver_path = "chrome-driver-path"
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)
driver = webdriver.Chrome(executable_path=chrome_driver_path, options=chrome_options)

# input in google forms
for i in range(len(listing_links)):
    driver.get(google_form)

    time.sleep(3)
    price_prompt = driver.find_element(By.XPATH,
                                       '/html/body/div/div[2]/form/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
    address_prompt = driver.find_element(By.XPATH,
                                         '/html/body/div/div[2]/form/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')

    link_prompt = driver.find_element(By.XPATH,
                                      '/html/body/div/div[2]/form/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
    submit_btn = driver.find_element(By.XPATH, '/html/body/div/div[2]/form/div[2]/div/div[3]/div[1]/div[1]/div')

    price_prompt.send_keys(prices[i])
    address_prompt.send_keys(addresses[i])
    link_prompt.send_keys(listing_links[i])

    submit_btn.click()

