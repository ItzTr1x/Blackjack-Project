import tkinter as tk
import random


class GUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("537x737")
        self.root.title("The Blackjack Project")
        self.name_entry = tk.StringVar()
        self.elements = {}

    def create_frame(self, name, row):
        self.elements[name] = tk.Frame(self.root, padx=10, pady=10)
        self.elements[name].grid(row=row, column=0, padx=5, pady=5)
        return name

    def loop(self):
        self.root.mainloop()

    def wait(self, varname):
        self.root.waitvar(varname)

    def leave(self):
        self.root.destroy()
        quit()

    def addImage(self, frame, image, width, height, caption, row, col, cspan=1):
        key = random.random()
        element = tk.Label(
            self.elements[frame],
            text=caption,
            image=image,
            compound="top",
            height=height,
            width=width,
        )
        element.grid(row=row, column=col, columnspan=cspan, padx=20, pady=10)
        self.elements[key] = element
        return key

    def addLabel(self, frame, content, row, col, width=1):
        key = random.random()
        element = tk.Label(self.elements[frame], text=content)
        element.grid(row=row, column=col, columnspan=width, padx=20, pady=10)
        self.elements[key] = element
        return key

    # just in case I can differentiate later
    def addText(self, frame, content, row, col, width=1):
        key = random.random()
        element = tk.Label(self.elements[frame], text=content)
        element.grid(row=row, column=col, columnspan=width, padx=20, pady=10)
        self.elements[key] = element
        return key

    def addTextInput(self, frame, textvariable, row, col, width=1):
        key = random.random()
        element = tk.Entry(self.elements[frame], textvariable=textvariable)
        element.grid(row=row, column=col, columnspan=width, padx=20, pady=10)
        self.elements[key] = element
        return key

    def addSubmit(self, frame, caption, command, row, col, width=1):
        key = random.random()
        element = tk.Button(self.elements[frame], text=caption, command=command)
        element.grid(row=row, column=col, columnspan=width, padx=20, pady=10)
        self.elements[key] = element
        return key

    def addRadio(
        self, frame, caption, variable, value, command, row, col, width=1, image=None
    ):
        key = random.random()
        element = tk.Radiobutton(
            self.elements[frame],
            variable=variable,
            value=value,
            text=caption,
            image=image,
            compound="top",
            indicatoron=False,
            command=command,
        )
        element.grid(column=col, row=row, padx=20, pady=10)
        self.elements[key] = element
        return key

    def getVariable(self, type):
        match type.lower():
            case "string":
                return tk.StringVar()
            case "int":
                return tk.IntVar()

    def kill(self, key):
        if key in self.elements:
            element = self.elements.pop(key)
            element.destroy()
