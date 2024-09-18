from data_manager import DataManager
from web_data import WebData

products_data = DataManager()
products = products_data.get_products()
amazon = WebData()
alert_data = {}
for product in products:
    product_price = amazon.process_amazon_data(product["LINK"])
    if product_price[1] < product["PRICE"]:
        alert_data[product_price[0]] = [product_price[1], product["LINK"], product["PRICE"]]
if len(alert_data)>0:
    pass