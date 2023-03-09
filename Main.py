import requests
import json
import tkinter as tk
import os

api_key = os.environ.get('API_KEY')
if not api_key:
    raise ValueError("API key not found")
base_url = "https://openexchangerates.org/api/latest.json"

class CurrencyConverter:
    def __init__(self, master):
        self.master = master
        master.title("Currency Converter")

        # Get screen dimensions
        screen_width = master.winfo_screenwidth()
        screen_height = master.winfo_screenheight()

        # Set window size and position
        width = 300
        height = 200
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        master.geometry(f"{width}x{height}+{x}+{y}")

        self.base_label = tk.Label(master, text="Base currency:")
        self.base_label.pack()

        self.base_options = self.get_currency_options()
        self.base_var = tk.StringVar(master)
        self.base_var.set(self.base_options[0])
        self.base_menu = tk.OptionMenu(master, self.base_var, *self.base_options)
        self.base_menu.pack()

        self.target_label = tk.Label(master, text="Target currency:")
        self.target_label.pack()

        self.target_options = self.get_currency_options()
        self.target_var = tk.StringVar(master)
        self.target_var.set(self.target_options[1])
        self.target_menu = tk.OptionMenu(master, self.target_var, *self.target_options)
        self.target_menu.pack()


        self.amount_label = tk.Label(master, text="Amount:")
        self.amount_label.pack()

        self.amount_entry = tk.Entry(master)
        self.amount_entry.pack()

        self.calculate_button = tk.Button(master, text="Calculate", command=self.calculate)
        self.calculate_button.pack()

        self.result_label = tk.Label(master, text="")
        self.result_label.pack()

    def get_currency_options(self):
        response = requests.get(base_url, params={"app_id": api_key})
        if response.status_code != 200:
            raise Exception("Failed to get exchange rates")
        data = json.loads(response.text)
        return ["USD"] + list(data["rates"].keys())

    def get_exchange_rates(self):
        response = requests.get(base_url, params={"app_id": api_key})
        if response.status_code != 200:
            raise Exception("Failed to get exchange rates")
        data = json.loads(response.text)
        return data["rates"]

    def calculate(self):
        base_currency = self.base_var.get()
        target_currency = self.target_var.get()
        amount = float(self.amount_entry.get())

        rates = self.get_exchange_rates()
        base_rate = rates.get(base_currency)
        target_rate = rates.get(target_currency)
        if not base_rate or not target_rate:
            self.result_label.config(text="Invalid currency")
        else:
            exchange_amount = amount * (target_rate / base_rate)
            self.result_label.config(text=f"{amount} {base_currency} is equivalent to {exchange_amount:.2f} {target_currency}")

root = tk.Tk()
converter = CurrencyConverter(root)
root.mainloop()

