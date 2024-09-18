import logging

from data_manager import DataManager
from user_alert import UserAlert
from web_data import WebData

logging.basicConfig(filename="logs.log", filemode="a", format="%(name)s → %(levelname)s: %(message)s)")

products_data = DataManager()
products = products_data.get_products()
amazon = WebData()
alert = UserAlert()
if products is None:
    print("No data to process")
    logging.warning("No data to process")
else:
    for product in products:
        if type(product["Amazon Product Link"]) is float:
            print("Invalid link to process")
            logging.warning("Invalid link to process")
        else:
            product_price = amazon.process_amazon_data(product["Amazon Product Link"])
            if product_price is None:
                print("No data to process")
                logging.warning("Unable to web scrap")
            else:
                if product_price[1] < int(product["Price Expected"]):
                    alert.alert_user(
                        client_name=f"{product['First Name']} {product['Last Name']}",
                        client_email=product["Email"],
                        product_name=product_price[0],
                        live_price=product_price[1],
                        expected_price=product["Price Expected"],
                        product_link=product["Amazon Product Link"]
                    )
