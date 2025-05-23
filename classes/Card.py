import tkinter as tk


class Card:

    # Generate and shuffle the deck
    def __init__(self, name, face, back):
        self.name = name
        self.value = self.calculate()
        self.face = tk.PhotoImage(file=face)
        self.back = tk.PhotoImage(file=back)

    def calculate(self):
        value = 0
        valstring = self.name[1:2]
        if valstring in ["X", "J", "Q", "K"]:
            value = 10
        elif valstring == "A":
            value = 11
        else:
            value = int(valstring)

        return value
