from tkinter import messagebox

class IKEAMyntAtare2000:

	def starta(self):
		messagebox.showinfo(message = "Välkommen till IKEA Mynt Ätare 2000")

	def stoppa(self):
		messagebox.showinfo(message = "Hejdå!")
		
	def betala(self, pris: int):
		messagebox.showinfo(message = f"{pris} cent")