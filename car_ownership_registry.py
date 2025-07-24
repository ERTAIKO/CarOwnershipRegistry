import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3

class CarOwnershipRegistryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Car Ownership Registry")
        self.root.geometry("400x350")

        # Initialize SQLite database
        self.conn = sqlite3.connect("car_ownership_registry.db")
        self.create_table()

        # GUI Elements
        tk.Label(root, text="Owner Name:").grid(row=0, column=0, padx=10, pady=5, sticky="e")
        self.owner_entry = tk.Entry(root)
        self.owner_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(root, text="Car Make:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.make_entry = tk.Entry(root)
        self.make_entry.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(root, text="Car Model:").grid(row=2, column=0, padx=10, pady=5, sticky="e")
        self.model_entry = tk.Entry(root)
        self.model_entry.grid(row=2, column=1, padx=10, pady=5)

        tk.Label(root, text="Year:").grid(row=3, column=0, padx=10, pady=5, sticky="e")
        self.year_entry = tk.Entry(root)
        self.year_entry.grid(row=3, column=1, padx=10, pady=5)

        tk.Button(root, text="Save Record", command=self.save_record).grid(row=4, column=0, columnspan=2, pady=10)
        tk.Button(root, text="View Registry", command=self.view_registry).grid(row=5, column=0, columnspan=2, pady=10)

    def create_table(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS cars (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                owner_name TEXT NOT NULL,
                make TEXT NOT NULL,
                model TEXT NOT NULL,
                year INTEGER NOT NULL
            )
        ''')
        self.conn.commit()

    def save_record(self):
        owner_name = self.owner_entry.get().strip()
        make = self.make_entry.get().strip()
        model = self.model_entry.get().strip()
        year = self.year_entry.get().strip()

        # Basic validation
        if not owner_name or not make or not model or not year:
            messagebox.showerror("Error", "All fields are required!")
            return
        try:
            year = int(year)
            if year < 1886 or year > 2025:  # Assuming cars start from 1886 and can't be future models
                raise ValueError("Year must be between 1886 and 2025")
        except ValueError:
            messagebox.showerror("Error", "Year must be a valid number between 1886 and 2025!")
            return

        # Save to database
        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO cars (owner_name, make, model, year) VALUES (?, ?, ?, ?)", 
                       (owner_name, make, model, year))
        self.conn.commit()

        messagebox.showinfo("Success", "Car ownership record saved successfully!")
        self.owner_entry.delete(0, tk.END)
        self.make_entry.delete(0, tk.END)
        self.model_entry.delete(0, tk.END)
        self.year_entry.delete(0, tk.END)

    def view_registry(self):
        # Create a new window for the registry
        registry_window = tk.Toplevel(self.root)
        registry_window.title("Car Ownership Registry")
        registry_window.geometry("600x400")

        # Create Treeview to display data
        tree = ttk.Treeview(registry_window, columns=("ID", "Owner", "Make", "Model", "Year"), show="headings")
        tree.heading("ID", text="ID")
        tree.heading("Owner", text="Owner Name")
        tree.heading("Make", text="Make")
        tree.heading("Model", text="Model")
        tree.heading("Year", text="Year")
        tree.column("ID", width=50)
        tree.column("Owner", width=150)
        tree.column("Make", width=100)
        tree.column("Model", width=100)
        tree.column("Year", width=80)
        tree.pack(fill="both", expand=True, padx=10, pady=10)

        # Fetch and display data
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM cars")
        for row in cursor.fetchall():
            tree.insert("", tk.END, values=row)

    def __del__(self):
        # Close database connection when the app closes
        self.conn.close()

if __name__ == "__main__":
    root = tk.Tk()
    app = CarOwnershipRegistryApp(root)
    root.mainloop()


python car_ownership_registry.py

