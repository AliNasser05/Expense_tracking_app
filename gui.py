import tkinter as tk
from tkinter import messagebox, ttk
from utils import validate_amount
import database as db
from charts import plot_expenses

class ExpenseApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Expense Tracker (SQLite Edition)")
        self.root.geometry("500x400")
        self.root.resizable(False, False)

        db.init_db()

        # -------- Input Frame --------
        input_frame = tk.LabelFrame(root, text="Add Expense", padx=10, pady=10)
        input_frame.pack(fill="x", padx=10, pady=10)

        tk.Label(input_frame, text="Category").grid(row=0, column=0, sticky="w")
        self.category_entry = tk.Entry(input_frame)
        self.category_entry.grid(row=0, column=1, padx=5, pady=2, sticky="ew")

        tk.Label(input_frame, text="Description").grid(row=1, column=0, sticky="w")
        self.desc_entry = tk.Entry(input_frame)
        self.desc_entry.grid(row=1, column=1, padx=5, pady=2, sticky="ew")

        tk.Label(input_frame, text="Amount").grid(row=2, column=0, sticky="w")
        self.amount_entry = tk.Entry(input_frame)
        self.amount_entry.grid(row=2, column=1, padx=5, pady=2, sticky="ew")

        self.add_button = tk.Button(input_frame, text="Add Expense", command=self.add_expense)
        self.add_button.grid(row=3, column=0, columnspan=2, pady=5)

        input_frame.columnconfigure(1, weight=1)

        # -------- Buttons Frame --------
        button_frame = tk.Frame(root)
        button_frame.pack(fill="x", padx=10)

        self.summary_button = tk.Button(button_frame, text="Show Chart", command=self.show_chart)
        self.summary_button.pack(side="left", padx=5, pady=5)

        self.view_button = tk.Button(button_frame, text="View All Expenses", command=self.view_expenses)
        self.view_button.pack(side="left", padx=5, pady=5)

        # -------- Expenses Table --------
        table_frame = tk.LabelFrame(root, text="Recent Expenses", padx=5, pady=5)
        table_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.tree = ttk.Treeview(table_frame, columns=("Category", "Description", "Amount"), show="headings")
        self.tree.heading("Category", text="Category")
        self.tree.heading("Description", text="Description")
        self.tree.heading("Amount", text="Amount")

        self.tree.column("Category", width=120)
        self.tree.column("Description", width=200)
        self.tree.column("Amount", width=80, anchor="e")

        self.tree.pack(fill="both", expand=True)

        self.load_expenses()

    def add_expense(self):
        category = self.category_entry.get().strip()
        desc = self.desc_entry.get().strip()
        amount = validate_amount(self.amount_entry.get().strip())

        if not category or not desc or amount is None:
            messagebox.showerror("Error", "Invalid input")
            return

        db.add_expense(category, desc, amount)
        messagebox.showinfo("Success", f"Added {amount} to {category}")

        self.category_entry.delete(0, tk.END)
        self.desc_entry.delete(0, tk.END)
        self.amount_entry.delete(0, tk.END)

        self.load_expenses()

    def show_chart(self):
        summary = db.get_summary()
        if summary:
            plot_expenses(summary)
        else:
            messagebox.showinfo("Info", "No expenses recorded yet")

    def view_expenses(self):
        # Popup with full history
        expenses = db.get_all_expenses()
        if not expenses:
            messagebox.showinfo("Info", "No expenses recorded yet")
            return

        window = tk.Toplevel(self.root)
        window.title("All Expenses")
        window.geometry("500x300")

        tree = ttk.Treeview(window, columns=("Category", "Description", "Amount"), show="headings")
        tree.heading("Category", text="Category")
        tree.heading("Description", text="Description")
        tree.heading("Amount", text="Amount")

        tree.column("Category", width=120)
        tree.column("Description", width=250)
        tree.column("Amount", width=100, anchor="e")

        for exp in expenses:
            tree.insert("", tk.END, values=exp)

        tree.pack(fill="both", expand=True)

    def load_expenses(self):
        # Refresh table with recent expenses
        for row in self.tree.get_children():
            self.tree.delete(row)

        expenses = db.get_all_expenses()
        for exp in expenses[:10]:  # show only 10 latest
            self.tree.insert("", tk.END, values=exp)
