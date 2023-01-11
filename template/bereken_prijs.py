from tariefeenheden import Tariefeenheden
from pricing_table import PricingTable
from ui_info import UIPayment, UIClass, UIWay, UIDiscount, UIPayment, UIInfo

class prijs():
  def __init__( self, info: UIInfo ):
    self.info = info
    self.tariefeenheden: int = Tariefeenheden.get_tariefeenheden(info.from_station, info.to_station)
    # compute the column in the table based on choices
    self.table_column = 0
    if info.travel_class == UIClass.FirstClass:
      table_column = 3
    # then, on the discount
    if info.discount == UIDiscount.TwentyDiscount:
      table_column += 1
    elif info.discount == UIDiscount.FortyDiscount:
      table_column += 2
  def bereken_prijs( self ):
    # compute price
    price: float = PricingTable.get_price (self.tariefeenheden, self.table_column)
    print(self.tariefeenheden)
    if self.info.way == UIWay.Return:
      price *= 2
    # add 50 cents if paying with credit card
    if self.info.payment == UIPayment.CreditCard:
      price += 0.50
    return price
    


