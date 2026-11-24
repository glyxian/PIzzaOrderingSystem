import tkinter as tk
from tkinter import ttk, messagebox

pizza_prices = {
    "Supreme": 295,
    "Hawaiian": 270,
    "Four Cheese": 260,
    "Meat Lovers": 320,
    "Veggie": 230
}

size_prices = {
    "Small": 0,
    "Medium": 70,
    "Large": 140
}

topping_prices = {
    "Extra Cheese": 35,
    "Mushrooms": 45,
    "Olives": 40,
    "Jalapeños": 30
}

BG = "#fdf3e3"
PANEL = "#fffaf0"
RED = "#c0392b"
TEXT = "#3b2a20"

window = tk.Tk()
window.title("GLY - Pizza Ordering System")
window.geometry("860x520")
window.resizable(True, True)
window.configure(bg=BG)

pizza_var = tk.StringVar(value="Supreme")
size_var = tk.StringVar(value="Small")
quantity_var = tk.IntVar(value=1)

topping_vars = {}
for t in topping_prices:
    topping_vars[t] = tk.BooleanVar(value=False)

title = tk.Label(
    window,
    text="GLY PIZZA",
    font=("Verdana", 22, "bold"),
    bg=BG,
    fg=RED
)
title.pack(pady=12)

main_area = tk.Frame(window, bg=BG)
main_area.pack(fill="both", expand=True, padx=20)

order_frame = tk.Frame(main_area, bg=PANEL, padx=20, pady=15)
order_frame.pack(side="left", fill="y")

receipt_frame = tk.Frame(main_area, bg=BG)
receipt_frame.pack(side="right", fill="both", expand=True, padx=(20, 0))

tk.Label(
    order_frame,
    text="Pizza Flavor:",
    font=("Verdana", 11, "bold"),
    bg=PANEL,
    fg=TEXT
).pack(anchor="w")

pizza_dropdown = ttk.Combobox(
    order_frame,
    textvariable=pizza_var,
    values=list(pizza_prices.keys()),
    state="readonly",
    font=("Verdana", 10)
)
pizza_dropdown.pack(fill="x", pady=6)

tk.Label(
    order_frame,
    text="Size:",
    font=("Verdana", 11, "bold"),
    bg=PANEL,
    fg=TEXT
).pack(anchor="w", pady=(10, 3))

for size, price in size_prices.items():
    tk.Radiobutton(
        order_frame,
        text=f"{size} +₱{price}",
        variable=size_var,
        value=size,
        font=("Verdana", 10),
        bg=PANEL,
        fg=TEXT,
        selectcolor="white",
        activebackground=PANEL,
        activeforeground=TEXT
    ).pack(anchor="w")

tk.Label(
    order_frame,
    text="Extra Toppings:",
    font=("Verdana", 11, "bold"),
    bg=PANEL,
    fg=TEXT
).pack(anchor="w", pady=(10, 3))

for topping, price in topping_prices.items():
    tk.Checkbutton(
        order_frame,
        text=f"{topping} +₱{price}",
        variable=topping_vars[topping],
        font=("Verdana", 10),
        bg=PANEL,
        fg=TEXT,
        selectcolor="white",
        activebackground=PANEL,
        activeforeground=TEXT
    ).pack(anchor="w")

tk.Label(
    order_frame,
    text="Quantity 1-50:",
    font=("Verdana", 11, "bold"),
    bg=PANEL,
    fg=TEXT
).pack(anchor="w", pady=(10, 3))

quantity_spinbox = tk.Spinbox(
    order_frame,
    from_=1,
    to=50,
    textvariable=quantity_var,
    font=("Verdana", 11),
    width=8
)
quantity_spinbox.pack(anchor="w")


def place_order():
    pizza = pizza_var.get()
    size = size_var.get()

    try:
        quantity = int(quantity_var.get())
        if quantity < 1 or quantity > 50:
            raise ValueError
    except (ValueError, tk.TclError):
        messagebox.showerror(
            "Invalid Quantity",
            "Quantity must be a whole number from 1 to 50."
        )
        return

    sure = messagebox.askyesno(
        "Confirm Order",
        "Place this order?"
    )
    if not sure:
        return

    pizza_price = pizza_prices[pizza]
    size_price = size_prices[size]

    chosen = []
    for name, var in topping_vars.items():
        if var.get():
            chosen.append(name)

    topping_total = 0
    for name in chosen:
        topping_total += topping_prices[name]

    per_pizza = pizza_price + size_price + topping_total
    total = per_pizza * quantity

    receipt_text.delete("1.0", tk.END)
    receipt_text.insert(tk.END, "GLY PIZZA RECEIPT\n\n")
    receipt_text.insert(tk.END, f"Flavor:   {pizza} ₱{pizza_price}\n")
    receipt_text.insert(tk.END, f"Size:     {size} +₱{size_price}\n")

    if chosen:
        receipt_text.insert(tk.END, "Toppings:\n")
        for name in chosen:
            receipt_text.insert(tk.END, f"   {name}: ₱{topping_prices[name]}\n")
    else:
        receipt_text.insert(tk.END, "Toppings: none\n")

    receipt_text.insert(tk.END, f"\nPrice per pizza: ₱{per_pizza:,.2f}\n")
    receipt_text.insert(tk.END, f"Quantity:        {quantity}\n")
    receipt_text.insert(tk.END, "---------------------------------\n")
    receipt_text.insert(tk.END, f"TOTAL: ₱{total:,.2f}\n")
    receipt_text.insert(tk.END, "\nSalamat! Enjoy.\n")


def reset_order():
    pizza_var.set("Supreme")
    size_var.set("Small")
    quantity_var.set(1)

    for var in topping_vars.values():
        var.set(False)

    receipt_text.delete("1.0", tk.END)


button_frame = tk.Frame(order_frame, bg=PANEL)
button_frame.pack(pady=(18, 0))

order_button = tk.Button(
    button_frame,
    text="PLACE ORDER",
    font=("Verdana", 10, "bold"),
    bg=RED,
    fg="white",
    width=14,
    command=place_order
)
order_button.grid(row=0, column=0, padx=5)

reset_button = tk.Button(
    button_frame,
    text="RESET",
    font=("Verdana", 10, "bold"),
    bg="#8c7b6b",
    fg="white",
    width=9,
    command=reset_order
)
reset_button.grid(row=0, column=1, padx=5)

tk.Label(
    receipt_frame,
    text="ORDER SUMMARY",
    font=("Verdana", 13, "bold"),
    bg=BG,
    fg=RED
).pack(anchor="w", pady=(0, 6))

receipt_text = tk.Text(
    receipt_frame,
    height=18,
    width=40,
    font=("Courier New", 11),
    bg="white",
    fg=TEXT
)
receipt_text.pack(fill="both", expand=True)

window.mainloop()