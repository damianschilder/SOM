from tariefeenheden import Tariefeenheden
from pricing_table import PricingTable
from ui_info import UIPayment, UIClass, UIWay, UIDiscount, UIPayment, UIInfo

class prijs():
  def __init__( self, info: UIInfo ):
    self.table_column = 0
    self.info = info
    self.tariefeenheden: int = Tariefeenheden.get_tariefeenheden(info.from_station, info.to_station)
    # compute the column in the table based on choices
    if info.travel_class == UIClass.FirstClass:
      self.table_column = 3
    # then, on the discount
    if info.discount == UIDiscount.TwentyDiscount:
      self.table_column += 1
    elif info.discount == UIDiscount.FortyDiscount:
      self.table_column += 2
  def bereken_prijs( self, amount ):
    # compute price
    price: float = PricingTable.get_price (self.tariefeenheden, self.table_column)
    print(self.tariefeenheden)
    if self.info.way == UIWay.Return:
      price *= 2
    # add 50 cents if paying with credit card
    if self.info.payment == UIPayment.CreditCard:
      price += 0.50
    price = price * amount
    return price
    


