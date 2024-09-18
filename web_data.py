import requests
from bs4 import BeautifulSoup


class WebData:
    def __init__(self):
        self.amazon_data = {}

    def process_amazon_data(self, url) -> list:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWeb"
                          "Kit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36"
        }
        try:
            response = requests.get(url, headers=headers)
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
        except ValueError:
            print("Unable val to process scrapping")
        except IndexError:
            print("Unable ind to process scrapping")
        except AttributeError:
            print("Unable conn to process scrapping")
        else:
            return return_data
