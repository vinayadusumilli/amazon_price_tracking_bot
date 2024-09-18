import requests
from bs4 import BeautifulSoup


class WebData:
    def __init__(self):
        self.amazon_data = {}

    def process_amazon_data(self, url) -> list:
        response = requests.get(url)
        web_data = response.text
        soup = BeautifulSoup(web_data, features="html.parser")
        product_name = soup.find(name="span", id="productTitle").get_text().strip()
        price_data = soup.find(name="span", class_="a-price-whole")
        decimal_price = soup.find(name="span", class_="a-price-fraction")
        product_price = price_data.get_text()
        price = product_price.replace(",", "")
        final_today_price = float(format(float(f"{price}{decimal_price.get_text()}"), ".2f"))
        self.amazon_data[product_name] = final_today_price
        return_data = [product_name, final_today_price]
        return return_data
