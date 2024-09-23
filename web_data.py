import time
import logging
from amazoncaptcha import AmazonCaptcha
from icecream import ic
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# Configure logging
logging.basicConfig(level=logging.INFO)


class WebData:
    def __init__(self):
        self.driver = None
        self.data: list = []

    def check_element_found(self, by, value) -> bool:
        try:
            logging.info("Checking for element...")
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((by, value))
            )
            return True
        except (TimeoutException, NoSuchElementException):
            logging.warning("Element not found")
            return False

    def get_products(self):
        try:
            product_name_element = self.driver.find_element(By.ID, "productTitle")
            product_name = product_name_element.text.strip()

            # Wait for the price element to be present
            price_xpath = '//*[@id="corePriceDisplay_desktop_feature_div"]/div[1]/span[3]/span[2]/span[2]'
            whole_price_element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, price_xpath))
            )
            whole_price_text = whole_price_element.text.strip()

            if whole_price_text:
                price = float(whole_price_text.replace(",", "").replace("$", ""))
                self.data = [product_name, price]
                ic(product_name, price)
                return True
            else:
                logging.warning("Price element is empty. Retrying...")
                return False
        except (NoSuchElementException, TimeoutException, ValueError) as e:
            logging.error(f"Error retrieving product details: {e}")
            return False

    def clear_captcha(self):
        try:
            captcha_prompt = self.driver.find_element(By.XPATH,
                                                      '/html/body/div[1]/div[1]/div[3]/div/div/form/div[1]/div/div/h4').text

            if "Type the characters you see in this image:" in captcha_prompt:
                img_captcha = self.driver.find_element(By.XPATH,
                                                       "/html/body/div[1]/div[1]/div[3]/div/div/form/div[1]/div/div/div[1]/img")
                captcha_link = img_captcha.get_attribute("src")
                captcha_solver = AmazonCaptcha.fromlink(captcha_link)
                captcha_value = captcha_solver.solve()

                captcha_input = self.driver.find_element(By.NAME, "field-keywords")
                captcha_input.send_keys(captcha_value)
                captcha_input.send_keys(Keys.ENTER)
                time.sleep(2)  # Allow time for captcha to be processed
                return True
        except NoSuchElementException:
            return True  # Captcha not found, proceed to the next retry
        except Exception as e:
            logging.error(f"Unexpected error while solving CAPTCHA: {e}")
            return False

    def process_amazon_data(self, url):
        retry = 6
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--enable-logging")
        chrome_options.add_argument("--v=1")
        chrome_options.add_argument("--remote-debugging-port=9222")

        self.driver = webdriver.Chrome(options=chrome_options)
        try:
            for attempt in range(retry):
                self.driver.get(url)
                ic(url)

                if self.check_element_found(By.ID, "productTitle"):
                    logging.info("Product found on Amazon")
                    if self.get_products():
                        break  # Exit the retry loop if successful
                elif self.check_element_found(By.XPATH,
                                              '/html/body/div[1]/div[1]/div[3]/div/div/form/div[1]/div/div/h4'):
                    logging.info("CAPTCHA encountered on Amazon")
                    if self.clear_captcha():
                        logging.info("CAPTCHA cleared..")
                        if self.check_element_found(By.ID, "productTitle"):
                            if self.get_products():
                                break  # Exit the retry loop if successful
                else:
                    logging.warning("Unable to get data from Amazon")
                time.sleep(5)  # General retry wait time
        except Exception as e:
            logging.error(f"An error occurred: {e}")
        finally:
            self.driver.quit()  # Ensure the driver is closed properly
