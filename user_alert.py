import os
import smtplib

from dotenv import load_dotenv

load_dotenv()

EMAIL = os.getenv("MY_EMAIL")
PASSWORD = os.getenv("MY_EMAIL_TOKEN")


class UserAlert:
    def __init__(self) -> None:
        self.gmail_smtp = "smtp.gmail.com"

    def alert_user(self, client_name, client_email, product_name, live_price, expected_price, product_link):
        with smtplib.SMTP(self.gmail_smtp) as connection:
            connection.starttls()
            connection.login(user=EMAIL, password=PASSWORD)
            connection.sendmail(from_addr=EMAIL,
                                to_addrs=client_email,
                                msg=f"Subject:Amazon Offer Alert!\n\nHi {client_name},\n\n"
                                    f"Great time to buy \"{product_name}\", "
                                    f"now price drop to \"{live_price}\" "
                                    f"and your waiting to buy price is \"{expected_price}\" "
                                    f"amazon link to buy {product_link}\n\n"
                                    f"Your personal assistant,\nPython Bot")
