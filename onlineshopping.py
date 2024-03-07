import tkinter as tk
from tkinter import messagebox
import mysql.connector

# MySQL connection
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Prateeth123@",
    database="onlineshopping"
)
cursor = mydb.cursor()

# Define Product class
class Product:
    def __init__(self, product_id, name, price, stock_quantity):
        self.product_id = product_id
        self.name = name
        self.price = price
        self.stock_quantity = stock_quantity

    def display_info(self):
        return f"Product ID: {self.product_id}\nName: {self.name}\nPrice: ${self.price}\nStock Quantity: {self.stock_quantity}"

# Define User class
class User:
    def __init__(self, user_id, username, password):
        self.user_id = user_id
        self.username = username
        self.password = password

    def login(self, username, password):
        # Check if username and password match in the database
        cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
        user = cursor.fetchone()
        if user:
            return True
        else:
            return False

    def signup(self, username, password):
        # Check if username already exists in the database
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        existing_user = cursor.fetchone()
        if existing_user:
            return False
        else:
            # Insert new user into the database
            cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
            mydb.commit()
            return True

    def order_history(self, user_id):
        # Retrieve order history for the given user
        cursor.execute("SELECT * FROM orders WHERE user_id = %s", (user_id,))
        orders = cursor.fetchall()
        return orders

# Define ShoppingCart class
class ShoppingCart:
    def __init__(self):
        self.products = []

    def add_product(self, product):
        self.products.append(product)

    def remove_product(self, product):
        self.products.remove(product)

    def display_cart(self):
        for product in self.products:
            print(product.display_info())

# GUI implementation using Tkinter
class OnlineShoppingGUI:
    def __init__(self, master):
        self.master = master
        master.title("Online Shopping System")

        # Define GUI elements
        self.login_frame = tk.Frame(master)
        self.username_label = tk.Label(self.login_frame, text="Username:")
        self.username_label.grid(row=0, column=0)
        self.username_entry = tk.Entry(self.login_frame)
        self.username_entry.grid(row=0, column=1)

        self.password_label = tk.Label(self.login_frame, text="Password:")
        self.password_label.grid(row=1, column=0)
        self.password_entry = tk.Entry(self.login_frame, show="*")
        self.password_entry.grid(row=1, column=1)

        self.login_button = tk.Button(self.login_frame, text="Login", command=self.login)
        self.login_button.grid(row=2, column=0, columnspan=2)

        self.signup_button = tk.Button(self.login_frame, text="Signup", command=self.signup)
        self.signup_button.grid(row=3, column=0, columnspan=2)

        self.shopping_frame = tk.Frame(master)
        self.order_history_frame = tk.Frame(master)
        self.order_history_text = tk.Text(self.order_history_frame, width=50, height=20)

        # Initialize as logged out state
        self.show_login()

    def show_login(self):
        self.shopping_frame.pack_forget()
        self.order_history_frame.pack_forget()
        self.order_history_text.pack_forget()
        self.login_frame.pack()

    def show_shopping(self):
        self.login_frame.pack_forget()
        self.order_history_frame.pack_forget()
        self.order_history_text.pack_forget()
        self.shopping_frame.pack()

    def show_order_history(self):
        self.login_frame.pack_forget()
        self.shopping_frame.pack_forget()
        self.order_history_frame.pack()
        self.order_history_text.pack()

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        user = User(0, username, password)
        if user.login(username, password):
            messagebox.showinfo("Login Successful", "Welcome back!")
            self.show_shopping()  # Redirect to shopping page
        else:
            messagebox.showerror("Login Failed", "Invalid username or password.")

    def signup(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        user = User(0, username, password)
        if user.signup(username, password):
            messagebox.showinfo("Signup Successful", "Account created successfully.")
        else:
            messagebox.showerror("Signup Failed", "Username already exists.")

    def display_order_history(self):
        user_id = 1  # Get the logged-in user's ID
        user = User(user_id, "", "")
        orders = user.order_history(user_id)
        self.order_history_text.insert(tk.END, "Order History:\n\n")
        for order in orders:
            self.order_history_text.insert(tk.END, f"Order ID: {order[0]}\n")
            self.order_history_text.insert(tk.END, f"Product ID: {order[2]}, Quantity: {order[3]}\n")
            self.order_history_text.insert(tk.END, f"Order Date: {order[4]}\n\n")

def main():
    # Initialize Tkinter GUI
    root = tk.Tk()
    app = OnlineShoppingGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
