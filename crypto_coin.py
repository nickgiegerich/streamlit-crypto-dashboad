class Coin:

    def __init__(self, coin_name, date_from, date_to):
        self.coin_name = coin_name
        self.date_from = date_from
        self.date_to = date_to

    def set_coin_name(self, coin_name):
        self.coin_name = coin_name

    def set_date_from(self, date_from):
        self.date_from = date_from

    def set_date_to(self, date_to):
        self.date_to = date_to

    def get_coin_name(self):
        return self.coin_name

    def get_date_from(self):
        return self.date_from

    def get_date_to(self):
        return self.date_to