from tariefeenheden import Tariefeenheden
import tkinter as tk
from bereken_prijs import prijs
from betaling import betaling
from pricing_table import PricingTable
from creditcard import CreditCard
from debitcard import DebitCard
from coin_machine import IKEAMyntAtare2000
from ui_info import UIPayment, UIClass, UIWay, UIDiscount, UIPayment, UIInfo


class UI(tk.Frame):

  def __init__(self, master):
    tk.Frame.__init__(self, master)
    self.widgets()

  def handle_payment(self, info: UIInfo):
    price = prijs( info )
    price = price.bereken_prijs()
    betaling( info, price )
    #region UI Set-up below -- you don't need to change anything

  def widgets(self):
    self.master.title("Ticket machine")
    menubar = tk.Menu(self.master)
    self.master.config(menu=menubar)

    fileMenu = tk.Menu(menubar)
    fileMenu.add_command(label="Exit", command=self.on_exit)
    menubar.add_cascade(label="File", menu=fileMenu)

    # retrieve the list of stations
    data2 = Tariefeenheden.get_stations()

    stations_frame = tk.Frame(self.master, highlightbackground="#cccccc", highlightthickness=1)
    stations_frame.pack(fill=tk.BOTH, expand=1, padx=10, pady=10)
    # From station
    tk.Label(stations_frame, text = "From station:").grid(row=0, padx=5, sticky=tk.W)
    self.from_station = tk.StringVar(value=data2[0])
    tk.OptionMenu(stations_frame, self.from_station, *data2).grid(row=1, padx=5, sticky=tk.W)

    # To station
    tk.Label(stations_frame, text = "To station:").grid(row=0, column=1, sticky=tk.W)
    self.to_station = tk.StringVar(value=data2[0])
    tk.OptionMenu(stations_frame, self.to_station, *data2).grid(row=1, column=1, sticky=tk.W)

    ticket_options_frame = tk.Frame(self.master, highlightbackground="#cccccc", highlightthickness=1)
    ticket_options_frame.pack(fill=tk.BOTH, expand=1, padx=10)

    # Class
    tk.Label(ticket_options_frame, text = "Travel class:").grid(row=1, sticky=tk.W)
    self.travel_class = tk.IntVar(value=UIClass.SecondClass.value)
    tk.Radiobutton(ticket_options_frame, text="First class", variable=self.travel_class, value=UIClass.FirstClass.value).grid(row=5, sticky=tk.W)
    tk.Radiobutton(ticket_options_frame, text="Second class", variable=self.travel_class, value=UIClass.SecondClass.value).grid(row=6, sticky=tk.W)

    # Way
    tk.Label(ticket_options_frame, text = "Way:").grid(row=7, sticky=tk.W)
    self.way = tk.IntVar(value=UIWay.OneWay.value)
    tk.Radiobutton(ticket_options_frame, text="One-way", variable=self.way, value=UIWay.OneWay.value).grid(row=8, sticky=tk.W)
    tk.Radiobutton(ticket_options_frame, text="Return", variable=self.way, value=UIWay.Return.value).grid(row=9, sticky=tk.W)

    # Discount
    tk.Label(ticket_options_frame, text = "Discount:").grid(row=10, sticky=tk.W)
    self.discount = tk.IntVar(value=UIDiscount.NoDiscount.value)
    tk.Radiobutton(ticket_options_frame, text="No discount", variable=self.discount, value=UIDiscount.NoDiscount.value).grid(row=11, sticky=tk.W)
    tk.Radiobutton(ticket_options_frame, text="20% discount", variable=self.discount, value=UIDiscount.TwentyDiscount.value).grid(row=12, sticky=tk.W)
    tk.Radiobutton(ticket_options_frame, text="40% discount", variable=self.discount, value=UIDiscount.FortyDiscount.value).grid(row=13, sticky=tk.W)

    payment_frame = tk.Frame(self.master, highlightbackground="#cccccc", highlightthickness=1)
    payment_frame.pack(fill=tk.BOTH, expand=1, padx=10, pady=10)

    # Payment
    tk.Label(payment_frame, text = "Payment:").grid(row=14, sticky=tk.W)
    self.payment = tk.IntVar(value=UIPayment.Cash.value)
    tk.Radiobutton(payment_frame, text="Cash", variable=self.payment, value=UIPayment.Cash.value).grid(row=15, sticky=tk.W)
    tk.Radiobutton(payment_frame, text="Credit Card", variable=self.payment, value=UIPayment.CreditCard.value).grid(row=16, sticky=tk.W)
    tk.Radiobutton(payment_frame, text="Debit Card", variable=self.payment, value=UIPayment.DebitCard.value).grid(row=17, sticky=tk.W)

    # Pay button
    tk.Button(self.master, text="Pay", command=self.on_click_pay).pack(side=tk.RIGHT, ipadx=10, padx=10, pady=10)

    self.pack(fill=tk.BOTH, expand=1)
  
  def on_click_pay(self):
    self.handle_payment(self.get_ui_info())

  def get_ui_info(self) -> UIInfo:
    return UIInfo(from_station=self.from_station.get(),
      to_station=self.to_station.get(),
      travel_class=self.travel_class.get(),
      way=self.way.get(),
      discount=self.discount.get(),
      payment=self.payment.get())

  def on_exit(self):
    self.quit()

#endregion


def main():

  root = tk.Tk()
  UI(root)

  root.mainloop()


if __name__ == '__main__':
  main()
