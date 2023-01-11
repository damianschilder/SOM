from card import Card
from tkinter import messagebox

# Mock CreditCard implementation
class CreditCard(Card):

    def connect(self):
        messagebox.showinfo(message = "Connecting to credit card reader")

    def disconnect(self):
        messagebox.showinfo(message = "Disconnecting from credit card reader")

    def begin_transaction(self, amount: float) -> int:
        messagebox.showinfo(message = f"Begin transaction 1 of {amount} EUR")
        return 1

    def end_transaction(self, id: int) -> bool:
        if id != 1:
            return False

        messagebox.showinfo(message = "End transaction 1")
        return True

    def cancel_transaction(self, id: int):
        if id != 1:
            raise Exception ("Incorrect transaction id")

        messagebox.showinfo(message = "Cancel transaction 1")
