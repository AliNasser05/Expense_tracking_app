import tkinter as tk
from gui import ExpenseApp

if __name__ == "__main__":
    root = tk.Tk()
    app = ExpenseApp(root)
    root.mainloop()
