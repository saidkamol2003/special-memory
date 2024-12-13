import tkinter as tk
import csv
from tkinter import messagebox
from tkinter import ttk

def create_main_window():
    root = tk.Tk()
    root.title("Car Inventory System")
    root.geometry("1200x400")

    root.grid_rowconfigure(1, weight=1)
    root.grid_columnconfigure(0, weight=1)

    notebook = ttk.Notebook(root)
    notebook.grid(row=0, column=0, sticky="ew")

    cars_tab = ttk.Frame(notebook)
    customers_tab = ttk.Frame(notebook)
    notebook.add(cars_tab, text="Cars")
    notebook.add(customers_tab, text="Customers")

    cars_tab.grid_rowconfigure(0, weight=1)
    cars_tab.grid_columnconfigure(0, weight=3)
    cars_tab.grid_columnconfigure(1, weight=1)

    display_frame = ttk.Frame(cars_tab, relief="raised", borderwidth=2)
    display_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

    tree = ttk.Treeview(
        display_frame, columns=("ID", "Make", "Model", "Year", "Price"), show="headings"
    )
    tree.heading("ID", text="ID")
    tree.heading("Make", text="Make")
    tree.heading("Model", text="Model")
    tree.heading("Year", text="Year")
    tree.heading("Price", text="Price")
    tree.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

    scrollbar = ttk.Scrollbar(display_frame, orient="vertical", command=tree.yview)
    scrollbar.grid(row=0, column=1, sticky="ns")
    tree.configure(yscrollcommand=scrollbar.set)

    display_frame.grid_rowconfigure(0, weight=1)
    display_frame.grid_columnconfigure(0, weight=1)

    crud_frame = ttk.Frame(cars_tab)
    crud_frame.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)

    ttk.Button(crud_frame, command=lambda: add_car(tree), text="Add New Car").grid(
        row=0, column=0, pady=10, padx=5, sticky="ew"
    )
    ttk.Button(
        crud_frame, command=lambda: edit_car(tree), text="Edit Selected Car"
    ).grid(row=1, column=0, pady=10, padx=5, sticky="ew")

    ttk.Button(
        crud_frame, text="Delete Selected Car", command=lambda: delete_car(tree)
    ).grid(row=2, column=0, pady=10, padx=5, sticky="ew")

    ttk.Button(crud_frame, text="Refresh List").grid(
        row=3, column=0, pady=10, padx=5, sticky="ew"
    )

    try:
        with open("cars.csv", "r") as file:
            reader = csv.reader(file)
            next(reader)

            for row in reader:
                tree.insert("", "end", values=row)
    except FileNotFoundError:
        pass

    return root

def add_car(tree):
    window = tk.Toplevel()
    window.title("Add new car")
    window.geometry("300x250")

    ttk.Label(window, text="Make: ").grid(row=0, column=0, padx=5, pady=5)
    make_input = ttk.Entry(window)
    make_input.grid(row=0, column=1)

    ttk.Label(window, text="Model: ").grid(row=1, column=0, padx=5, pady=5)
    model_input = ttk.Entry(window)
    model_input.grid(row=1, column=1)

    ttk.Label(window, text="Year: ").grid(row=2, column=0, padx=5, pady=5)
    year_input = ttk.Entry(window)
    year_input.grid(row=2, column=1)

    ttk.Label(window, text="Price: ").grid(row=3, column=0, padx=5, pady=5)
    price_input = ttk.Entry(window)
    price_input.grid(row=3, column=1)

    def save_car():
        make = make_input.get()
        model = model_input.get()
        year = year_input.get()
        price = price_input.get()

        if not all([make, model, year, price]):
            messagebox.showerror("Error", "Fill all fields")
            return

        try:
            try:
                with open("cars.csv", "r") as file:
                    reader = csv.reader(file)
                    next(reader)

                    cars = list(reader)
                    next_id = str(len(cars) + 1)
            except FileNotFoundError:
                with open("cars.csv", "w", newline="") as file:
                    writer = csv.writer(file)
                    writer.writerow(["ID", "Make", "Model", "Year", "Price"])
                    next_id = "1"

            with open("cars.csv", "a", newline="") as file:
                writer = csv.writer(file)
                writer.writerow([next_id, make, model, year, price])

            tree.insert("", "end", values=(next_id, make, model, year, price))
            messagebox.showinfo("Succcess", "Car added successfully")
        except Exception as e:
            messagebox.showerror("Error", f"Error occured: {str(e)}")

    ttk.Button(window, text="Save car", command=save_car).grid(
        row=4, column=0, columnspan=2, pady=20
    )

def edit_car(tree):
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showerror("Error", "Please select a car to edit")
        return

    car_values = tree.item(selected_item)["values"]

    window = tk.Toplevel()
    window.title("Edit Car")
    window.geometry("300x250")

    ttk.Label(window, text="Make: ").grid(row=0, column=0, padx=5, pady=5)
    make_input = ttk.Entry(window)
    make_input.insert(0, car_values[1])
    make_input.grid(row=0, column=1)

    ttk.Label(window, text="Model: ").grid(row=1, column=0, padx=5, pady=5)
    model_input = ttk.Entry(window)
    model_input.insert(0, car_values[2])
    model_input.grid(row=1, column=1)

    ttk.Label(window, text="Year: ").grid(row=2, column=0, padx=5, pady=5)
    year_input = ttk.Entry(window)
    year_input.insert(0, car_values[3])
    year_input.grid(row=2, column=1)

    ttk.Label(window, text="Price: ").grid(row=3, column=0, padx=5, pady=5)
    price_input = ttk.Entry(window)
    price_input.insert(0, car_values[4])
    price_input.grid(row=3, column=1)

    def save_changes():
        make = make_input.get()
        model = model_input.get()
        year = year_input.get()
        price = price_input.get()

        if not all([make, model, year, price]):
            messagebox.showerror("Error", "Fill all fields")
            return

        try:
            with open("cars.csv", "r") as file:
                cars = list(csv.reader(file))

            for car in cars:
                if car[0] == str(car_values[0]):
                    car[1:] = [make, model, year, price]
                    break

            with open("cars.csv", "w", newline="") as file:
                writer = csv.writer(file)
                writer.writerows(cars)

            tree.item(selected_item, values=(car_values[0], make, model, year, price))
            messagebox.showinfo("Success", "Car updated successfully")
            window.destroy()

        except Exception as e:
            messagebox.showerror("Error", f"Error occurred: {str(e)}")

    ttk.Button(window, text="Save Changes", command=save_changes).grid(
        row=4, column=0, columnspan=2, pady=20
    )

def delete_car(tree):
    selected_item = tree.selection()

    if not selected_item:
        messagebox.showerror("Error", "Please select a car to delete")
        return

    confirm = messagebox.askyesno(
        "Confirm Delete", "Are you sure you want to delete this car?"
    )

    if confirm:
        try:
            car_values = tree.item(selected_item)["values"]
            updated_cars = []

            with open("cars.csv", "r") as file:
                reader = csv.reader(file)
                header = next(reader)
                for row in reader:
                    if row[0] != str(car_values[0]):
                        updated_cars.append(row)

            with open("cars.csv", "w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(header)
                writer.writerows(updated_cars)

            tree.delete(selected_item)
            messagebox.showinfo("Success", "Car deleted successfully")

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

def main():
    root = create_main_window()
    root.mainloop()

def create_main_window():
    root = tk.Tk()
    root.title("Car Inventory System")
    root.geometry("1200x400")

    root.grid_rowconfigure(1, weight=1)
    root.grid_columnconfigure(0, weight=1)

    notebook = ttk.Notebook(root)
    notebook.grid(row=0, column=0, sticky="ew")

    cars_tab = ttk.Frame(notebook)
    customers_tab = ttk.Frame(notebook)
    notebook.add(cars_tab, text="Cars")
    notebook.add(customers_tab, text="Customers")

    # Cars Tab Layout
    cars_tab.grid_rowconfigure(0, weight=1)
    cars_tab.grid_columnconfigure(0, weight=3)
    cars_tab.grid_columnconfigure(1, weight=1)

    display_frame = ttk.Frame(cars_tab, relief="raised", borderwidth=2)
    display_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

    tree = ttk.Treeview(
        display_frame, columns=("ID", "Make", "Model", "Year", "Price"), show="headings"
    )
    tree.heading("ID", text="ID")
    tree.heading("Make", text="Make")
    tree.heading("Model", text="Model")
    tree.heading("Year", text="Year")
    tree.heading("Price", text="Price")
    tree.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

    scrollbar = ttk.Scrollbar(display_frame, orient="vertical", command=tree.yview)
    scrollbar.grid(row=0, column=1, sticky="ns")
    tree.configure(yscrollcommand=scrollbar.set)

    display_frame.grid_rowconfigure(0, weight=1)
    display_frame.grid_columnconfigure(0, weight=1)

    crud_frame = ttk.Frame(cars_tab)
    crud_frame.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)

    ttk.Button(crud_frame, command=lambda: add_car(tree), text="Add New Car").grid(
        row=0, column=0, pady=10, padx=5, sticky="ew"
    )
    ttk.Button(crud_frame, command=lambda: edit_car(tree), text="Edit Selected Car").grid(
        row=1, column=0, pady=10, padx=5, sticky="ew"
    )
    ttk.Button(crud_frame, text="Delete Selected Car", command=lambda: delete_car(tree)).grid(
        row=2, column=0, pady=10, padx=5, sticky="ew"
    )
    ttk.Button(crud_frame, text="Refresh List").grid(row=3, column=0, pady=10, padx=5, sticky="ew")

    # Customers Tab Layout
    customers_tab.grid_rowconfigure(0, weight=1)
    customers_tab.grid_columnconfigure(0, weight=3)
    customers_tab.grid_columnconfigure(1, weight=1)

    customer_display_frame = ttk.Frame(customers_tab, relief="raised", borderwidth=2)
    customer_display_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

    customer_tree = ttk.Treeview(
        customer_display_frame, columns=("ID", "Name", "Email", "Phone"), show="headings"
    )
    customer_tree.heading("ID", text="ID")
    customer_tree.heading("Name", text="Name")
    customer_tree.heading("Email", text="Email")
    customer_tree.heading("Phone", text="Phone")
    customer_tree.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

    customer_scrollbar = ttk.Scrollbar(customer_display_frame, orient="vertical", command=customer_tree.yview)
    customer_scrollbar.grid(row=0, column=1, sticky="ns")
    customer_tree.configure(yscrollcommand=customer_scrollbar.set)

    customer_display_frame.grid_rowconfigure(0, weight=1)
    customer_display_frame.grid_columnconfigure(0, weight=1)

    customer_crud_frame = ttk.Frame(customers_tab)
    customer_crud_frame.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)

    ttk.Button(customer_crud_frame, command=lambda: add_customer(customer_tree), text="Add New Customer").grid(
        row=0, column=0, pady=10, padx=5, sticky="ew"
    )
    ttk.Button(customer_crud_frame, command=lambda: edit_customer(customer_tree), text="Edit Selected Customer").grid(
        row=1, column=0, pady=10, padx=5, sticky="ew"
    )
    ttk.Button(customer_crud_frame, text="Delete Selected Customer", command=lambda: delete_customer(customer_tree)).grid(
        row=2, column=0, pady=10, padx=5, sticky="ew"
    )
    ttk.Button(customer_crud_frame, text="Refresh List").grid(row=3, column=0, pady=10, padx=5, sticky="ew")

    try:
        with open("customers.csv", "r") as file:
            reader = csv.reader(file)
            next(reader)  # Skip header row
            for row in reader:
                customer_tree.insert("", "end", values=row)
    except FileNotFoundError:
        pass

    return root

# Add New Customer
def add_customer(tree):
    window = tk.Toplevel()
    window.title("Add New Customer")
    window.geometry("300x250")

    ttk.Label(window, text="Name: ").grid(row=0, column=0, padx=5, pady=5)
    name_input = ttk.Entry(window)
    name_input.grid(row=0, column=1)

    ttk.Label(window, text="Email: ").grid(row=1, column=0, padx=5, pady=5)
    email_input = ttk.Entry(window)
    email_input.grid(row=1, column=1)

    ttk.Label(window, text="Phone: ").grid(row=2, column=0, padx=5, pady=5)
    phone_input = ttk.Entry(window)
    phone_input.grid(row=2, column=1)

    def save_customer():
        name = name_input.get()
        email = email_input.get()
        phone = phone_input.get()

        if not all([name, email, phone]):
            messagebox.showerror("Error", "Fill all fields")
            return

        try:
            try:
                with open("customers.csv", "r") as file:
                    reader = csv.reader(file)
                    next(reader)  # Skip header
                    customers = list(reader)
                    next_id = str(len(customers) + 1)
            except FileNotFoundError:
                with open("customers.csv", "w", newline="") as file:
                    writer = csv.writer(file)
                    writer.writerow(["ID", "Name", "Email", "Phone"])
                    next_id = "1"

            with open("customers.csv", "a", newline="") as file:
                writer = csv.writer(file)
                writer.writerow([next_id, name, email, phone])

            tree.insert("", "end", values=(next_id, name, email, phone))
            messagebox.showinfo("Success", "Customer added successfully")
        except Exception as e:
            messagebox.showerror("Error", f"Error occurred: {str(e)}")

    ttk.Button(window, text="Save customer", command=save_customer).grid(row=3, column=0, columnspan=2, pady=20)

# Edit Customer
def edit_customer(tree):
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showwarning("No selection", "Please select a customer to edit.")
        return

    customer_id = tree.item(selected_item)["values"][0]
    name = tree.item(selected_item)["values"][1]
    email = tree.item(selected_item)["values"][2]
    phone = tree.item(selected_item)["values"][3]

    window = tk.Toplevel()
    window.title("Edit Customer")
    window.geometry("300x250")

    ttk.Label(window, text="Name: ").grid(row=0, column=0, padx=5, pady=5)
    name_input = ttk.Entry(window)
    name_input.insert(0, name)
    name_input.grid(row=0, column=1)

    ttk.Label(window, text="Email: ").grid(row=1, column=0, padx=5, pady=5)
    email_input = ttk.Entry(window)
    email_input.insert(0, email)
    email_input.grid(row=1, column=1)

    ttk.Label(window, text="Phone: ").grid(row=2, column=0, padx=5, pady=5)
    phone_input = ttk.Entry(window)
    phone_input.insert(0, phone)
    phone_input.grid(row=2, column=1)

    def save_changes():
        new_name = name_input.get()
        new_email = email_input.get()
        new_phone = phone_input.get()

        if not all([new_name, new_email, new_phone]):
            messagebox.showerror("Error", "Fill all fields")
            return

        try:
            with open("customers.csv", "r") as file:
                reader = csv.reader(file)
                customers = list(reader)

            for i, customer in enumerate(customers):
                if customer[0] == customer_id:
                    customers[i] = [customer_id, new_name, new_email, new_phone]
                    break

            with open("customers.csv", "w", newline="") as file:
                writer = csv.writer(file)
                writer.writerows(customers)

            for item in tree.get_children():
                tree.delete(item)

            with open("customers.csv", "r") as file:
                reader = csv.reader(file)
                next(reader)  # Skip header
                for row in reader:
                    tree.insert("", "end", values=row)

            messagebox.showinfo("Success", "Customer updated successfully")
            window.destroy()

        except Exception as e:
            messagebox.showerror("Error", f"Error occurred: {str(e)}")

    ttk.Button(window, text="Save changes", command=save_changes).grid(row=3, column=0, columnspan=2, pady=20)

# Delete Customer
def delete_customer(tree):
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showwarning("No selection", "Please select a customer to delete.")
        return

    customer_id = tree.item(selected_item)["values"][0]
	
    response = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete customer {customer_id}?")
    if response:
        try:
            with open("customers.csv", "r") as file:
                reader = csv.reader(file)
                customers = list(reader)

            customers = [customer for customer in customers if customer[0] != customer_id]

            with open("customers.csv", "w", newline="") as file:
                writer = csv.writer(file)
                writer.writerows(customers)

            tree.delete(selected_item)
            messagebox.showinfo("Success", "Customer deleted successfully")

        except Exception as e:
            messagebox.showerror("Error", f"Error occurred: {str(e)}")

def main():
    root = create_main_window()
    root.mainloop()

if __name__ == "__main__":
    main()