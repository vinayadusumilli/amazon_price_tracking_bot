import pathlib
from data_manager import DataManager
from user_alert import UserAlert
from web_data import WebData
from icecream import ic

CURRENT_PATH = pathlib.Path(__file__).parent.resolve()

products_data = DataManager()
products = products_data.get_products()
amazon = WebData()
alert = UserAlert()

if products is None or len(products) == 0:
    print("No data to process")
else:
    for product in products:
        product_link = product.get("Amazon Product Link")
        if not isinstance(product_link, str) or not product_link.strip():
            print("Invalid link to process")
            continue

        print("Processing product:", product_link)
        try:
            amazon.process_amazon_data(product_link)
            product_price = amazon.data

            if product_price is None or len(product_price) == 0:
                print("No data retrieved for product:", product_link)
                continue

            ic(product_price, product["Price Expected"])
            if product_price[1] < int(product["Price Expected"]):
                print("Found offer for product:", product_price[0])
                alert.alert_user(
                    client_name=f"{product['First Name']} {product['Last Name']}",
                    client_email=product["Email"],
                    product_name=product_price[0],
                    live_price=product_price[1],
                    expected_price=product["Price Expected"],
                    product_link=product_link
                )
        except Exception as e:
            print(f"Error processing product {product_link}: {e}")
