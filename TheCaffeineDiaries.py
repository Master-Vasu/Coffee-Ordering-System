from rich.console import Console
from rich.table import Table
import re

# Initializing console
console = Console()

class Order:
    def __init__(self):
        self.items = []

    def add_item(self, option, coffee, rate, quantity, price):
        if self.is_empty():
            self.items.append({"option": option, "coffee": coffee, "rate": rate, "quantity": quantity, "price": price})
        else:
            for item in self.items:
                if item.get("option") == option:
                    self.update_item(option, quantity)
                    break
            else:
                self.items.append({"option": option, "coffee": coffee, "rate": rate, "quantity": quantity, "price": price})

    def update_item(self, option, qnt):
        for item in self.items:
            if item["option"] == option:
                item["quantity"] += qnt
                item["price"] = item["quantity"] * item["rate"]
                break

    def remove_item(self, option, qnt):
        for item in self.items:
            if item["option"] == option:
                if qnt < 0 or qnt > item["quantity"]:
                    return False
                elif item["quantity"] == qnt:
                    self.items.remove(item)
                    return True
                else:
                    item["quantity"] -= qnt
                    item["price"] = item["quantity"] * item["rate"]
                    return True

    def check_item(self, option):
        for item in self.items:
            if item.get("option") == option:
                return True
        return False

    def calculate_total(self):
        total = 0
        for item in self.items:
            total += item["rate"] * item["quantity"]
        return total

    def order_summary(self):
        if self.is_empty():
            console.print("\nOops! No items to order.", style="red")
        else:
            summary = Table(
                title='\n[bright_yellow]Order Summary:[bright_yellow]',
                caption='[bold dim magenta]Enter "A" to add coffee to your order.\nEnter "R" to remove a coffee from your order.\nEnter "M" to display the Menu.\nEnter "C" to checkout with your current order.[/bold dim magenta]\n',
                caption_style="normal")

            summary.add_column("OPTION", width=8, justify="center")
            summary.add_column("ITEMS", width=20, justify="left")
            summary.add_column("RATE (₹)", width=8, justify="center", style="green")
            summary.add_column("QUANTITY", width=8, justify="center")
            summary.add_column("TOTAL", width=10, justify="center", style="green")

            total = 0
            for entry in self.items:
                summary.add_row(str(entry["option"]), entry["coffee"], str(entry["rate"]), str(entry["quantity"]), f"[green]{str(entry['price'])}")
                total += entry["price"]

            total = "₹" + str(total)
            summary.add_row("", "", "", "", ""); summary.add_row("", "", "", "", "")
            summary.add_row("", "", "", "", f"[bold]{total}[/bold]")

            console.print(summary)

    def is_empty(self):
        return not self.items

class Menu:
    def __init__(self):
        self.items = [
            {"option": 1, "coffee": "Espresso", "rate": 199.99},
            {"option": 2, "coffee": "Classic Cold Brew", "rate": 279.99},
            {"option": 3, "coffee": "Tonic Cold", "rate": 299.99},
            {"option": 4, "coffee": "Cappuccino", "rate": 329.99},
            {"option": 5, "coffee": "Latte", "rate": 339.99},
            {"option": 6, "coffee": "Flat White", "rate": 329.99},
            {"option": 7, "coffee": "Hazelnut Frappe", "rate": 459.99},
            {"option": 8, "coffee": "French Press", "rate": 289.99},
            {"option": 9, "coffee": "Caffeine Blast", "rate": 999.99},
        ]

    def display_menu(self):
        menu = Table(
            title='\n\n[bright_yellow]Welcome to "The Caffeine Diaries"\n\nMenu[/bright_yellow]',
            caption='[bold dim magenta]Enter "A" to add coffee to your order.\nEnter "R" to remove a coffee from your order.\nEnter "M" to display the Menu.\nEnter "C" to checkout with your current order.[/bold dim magenta]\n',
            show_lines=True,
            caption_style="normal")

        menu.add_column("OPTION", width=10, justify="center")
        menu.add_column("COFFEES", width=24)
        menu.add_column("RATE (₹)", width=12, justify="center", style="bright_green")

        for item in self.items:
            menu.add_row(str(item["option"]), item["coffee"], str(item["rate"]))

        console.print(menu)

    def check_option(self, option):
        for item in self.items:
            if item.get("option") == option:
                return True
        return False

    def fetch_item(self, option):
        return self.items[option - 1]

class NoItemFound(Exception):
    pass

def main():
    order = Order()
    menu = Menu()

    menu.display_menu()

    choice = take_order(order)
    while choice != "C":
        if choice == "A":
            add_items_interactive(order, menu)
        elif choice == "R":
            remove_items_interactive(order)
        elif choice == "M":
            menu.display_menu()

        choice = take_order(order)

    checkout_interactive(order)

def take_order(order):
    while True:
        try:
            choice = input('Enter "A" or "R" or "C" or "M" to proceed: ')
            if matches := re.search(r"^(A|R|C|M)$", choice):
                break
            else:
                raise ValueError
        except ValueError:
            console.print('\n[red]Invalid input![/red], Please enter "A" or "R" or "C" or "M" to continue.')

    return matches.group(1)

def add_items(order, menu, option, qnt):
    item = menu.fetch_item(option)
    order.add_item(option, item["coffee"], item["rate"], qnt, item["rate"] * qnt)
    order.order_summary()

def remove_items(order, option, qnt):
    if order.is_empty():
        console.print("\nOops! No items in order to remove.", style="red")
    else:
        if not order.check_item(option):
            raise NoItemFound('\n[red]Invalid input![/red], Please enter valid option no. from your order summary.')

        if not order.remove_item(option, qnt):
            raise ValueError('\n[red]Invalid input![/red], Please enter quantity more than zero and less than actual quantity.')

        order.order_summary()

def checkout(order):
    if order.is_empty():
        console.print("\nOops! No items in order.", style="red")
        return "No items to checkout"
    else:
        return print_receipt(order)

def add_items_interactive(order, menu):
    while True:
        try:
            option = int(input("Enter option no. to add your coffee: "))
            if menu.check_option(option):
                break
            else:
                raise ValueError
        except ValueError:
            console.print('\n[red]Invalid input![/red], Please enter option no. between 1 and 9 from the menu.')

    while True:
        try:
            qnt = int(input("Enter no. of quantities of coffee to add: "))
            if qnt > 0:
                break
            else:
                raise ValueError
        except ValueError:
            console.print('\n[red]Invalid input![/red], Please enter quantity more than zero.')

    add_items(order, menu, option, qnt)

def remove_items_interactive(order):
    if order.is_empty():
        console.print("\nOops! No items in order to remove.", style="red")
    else:
        while True:
            try:
                option = int(input("Enter option no. from your order to be removed: "))
                if order.check_item(option):
                    break
                else:
                    raise NoItemFound
            except (ValueError, NoItemFound):
                console.print('\n[red]Invalid input![/red], Please enter valid option no. from your order summary.')

        while True:
            try:
                qnt = int(input("Enter no. of quantities of coffee to be removed: "))
                for item in order.items:
                    if order.remove_item(option, qnt):
                        break
                    else:
                        raise ValueError
                break
            except ValueError:
                console.print('\n[red]Invalid input![/red], Please enter quantity more than zero and less than actual quantity.')

    order.order_summary()

def checkout_interactive(order):
    if order.is_empty():
        console.print("\nOops! No items in order.", style="red")
    else:
        print_receipt(order)

def print_receipt(order):
    receipt = Table(
        title='\n\n[bright_yellow]Welcome to "The Caffeine Diaries"[/bright_yellow]',
        caption='\n[bright_yellow]Receipt[/bright_yellow]',
        show_lines=True,
        caption_style="bold")

    receipt.add_column("ITEMS", width=24, justify="left")
    receipt.add_column("RATE (₹)", width=8, justify="center", style="green")
    receipt.add_column("QUANTITY", width=8, justify="center")
    receipt.add_column("TOTAL", width=10, justify="center", style="green")

    total = 0
    for entry in order.items:
        receipt.add_row(entry["coffee"], str(entry["rate"]), str(entry["quantity"]), f"[green]{str(entry['price'])}")
        total += entry["price"]

    total = "₹" + str(total)
    receipt.add_row("", "", "", ""); receipt.add_row("", "", "", "")
    receipt.add_row("", "", "", f"[bold]{total}[/bold]")

    console.print(receipt)
    print("Thank you for your order. We look forward to serving you soon!")

if __name__ == "__main__":
    main()
