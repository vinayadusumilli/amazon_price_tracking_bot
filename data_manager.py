import pandas


class DataManager:
    def __init__(self) -> None:
        self.df = pandas.read_csv("products_data.csv")

    def get_products(self) -> list:
        return self.df.to_dict(orient="records")
