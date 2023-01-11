class PricingTable:

    @staticmethod
    def get_price(tariefeenheden: int, col: int) -> float:
        price = 0

        if col == 0:
            price = 2.10
        elif col == 1:
            price = 1.70
        elif col == 2:
            price = 1.30
        elif col == 3:
            price = 3.60
        elif col == 4:
            price = 2.90
        elif col == 5:
            price = 2.20
        else:
            raise Exception("Unknown column number")

        price = price * 0.02 * tariefeenheden
        return round(price, 2)
