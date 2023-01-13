from tariefeenheden import Tariefeenheden
import tkinter as tk
from calculate_price import cost
from payment import payment
from pricing_table import PricingTable
from creditcard import CreditCard
from debitcard import DebitCard
from coin_machine import IKEAMyntAtare2000
from ui_info import UIPayment, UIClass, UIWay, UIDiscount, UIPayment, UIInfo
from tkcalendar import Calendar
from datetime import datetime


class UI(tk.Frame):
  def __init__(self, master):
    tk.Frame.__init__(self, master)
    self.widgets()
  def handle_payment(self, info: UIInfo):
    price = cost( info )
    price = price.calculate_price( tkAmount.get() )
    payment( info, price )
  
  #region UI Set-up below -- you don't need to change anything

  def widgets(self):
    self.master.title("Ticket machine")
    menubar = tk.Menu(self.master)
    self.master.config(menu=menubar)
    self.master.geometry("1080x600")

    fileMenu = tk.Menu(menubar)
    fileMenu.add_command(label="Exit", command=self.on_exit)
    menubar.add_cascade(label="File", menu=fileMenu)

    # retrieve the list of stations
    data2 = Tariefeenheden.get_stations()

    # stations_frame = tk.Frame(self.master, highlightbackground="#cccccc", highlightthickness=1)
    # stations_frame.pack(fill=tk.BOTH, expand=1, padx=10, pady=10)
    stations_frame = tk.Canvas(self.master, highlightbackground="#cccccc", highlightthickness=1)
    stations_frame.pack(side=tk.LEFT,fill=tk.BOTH,expand=1)
    stations_frame.config(width=20, height=600)
    # From station
    tk.Label(stations_frame, text = "From station:").grid(row=0, padx=5, sticky=tk.W)
    self.from_station = tk.StringVar(value=data2[0])
    tk.OptionMenu(stations_frame, self.from_station, *data2).grid(row=1, padx=5, sticky=tk.W)

    # To station
    tk.Label(stations_frame, text = "To station:").grid(row=0, column=1, sticky=tk.W)
    self.to_station = tk.StringVar(value=data2[0])
    tk.OptionMenu(stations_frame, self.to_station, *data2).grid(row=1, column=1, sticky=tk.W)

    # ticket_options_frame = tk.Frame(self.master, highlightbackground="#cccccc", highlightthickness=1)
    # ticket_options_frame.pack(fill=tk.BOTH, expand=1, padx=10)
    ticket_options_frame = tk.Canvas(self.master, highlightbackground="#cccccc", highlightthickness=1)
    ticket_options_frame.pack(side=tk.LEFT,fill=tk.BOTH,expand=1, padx=10)
    stations_frame.config(width=260, height=600)


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

    # Amount
    global tkAmount
    tkAmount = tk.IntVar( value = 1)
    tk.Label(ticket_options_frame, text = 'Amount').grid(row=14, sticky=tk.W)
    tk.Label(ticket_options_frame, textvariable = tkAmount ).grid(row=15,  sticky=tk.W, padx=25)
    tk.Button(ticket_options_frame, text="-", command=self.deduct_amount).grid(row=15, sticky=tk.W)
    tk.Button(ticket_options_frame, text="+", command=self.add_amount).grid(row=15, sticky=tk.W, padx=45)

    tk.Label(ticket_options_frame, text = 'Date').grid(row=16, sticky=tk.W, pady=15)
    print(datetime.today().strftime('%m'))
    cal = Calendar(ticket_options_frame, selectmode = 'day', year = 2023, month = int(datetime.today().strftime('%m')), day = int(datetime.today().strftime('%d')))
    cal.grid(row=17, sticky=tk.W) 

    payment_frame = tk.Canvas(self.master)
    payment_frame.pack(side=tk.RIGHT,fill=tk.BOTH,expand=1)
    payment_frame.config(width=360, height=600)

    # Payment
    tk.Label(payment_frame, text = "Payment:").grid(row=0, sticky=tk.W)
    self.payment = tk.IntVar(value=UIPayment.Cash.value)
    tk.Radiobutton(payment_frame, text="Cash", variable=self.payment, value=UIPayment.Cash.value).grid(row=1, sticky=tk.W)
    tk.Radiobutton(payment_frame, text="Credit Card", variable=self.payment, value=UIPayment.CreditCard.value).grid(row=2, sticky=tk.W)
    tk.Radiobutton(payment_frame, text="Debit Card", variable=self.payment, value=UIPayment.DebitCard.value).grid(row=3, sticky=tk.W)

    # Pay button
    tk.Button(payment_frame, text="Pay", command=self.on_click_pay).grid(row=5, sticky=tk.W)

    self.pack(fill=tk.BOTH, expand=1)
  
  def deduct_amount(self):
    if (tkAmount.get() <= 1):
      return
    tkAmount.set(tkAmount.get() - 1)
    
  def add_amount(self):
    tkAmount.set(tkAmount.get() + 1)
  
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
