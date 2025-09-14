import matplotlib.pyplot as plt

def plot_expenses(summary):
    categories = list(summary.keys())
    amounts = list(summary.values())

    plt.figure(figsize=(6, 6))
    plt.pie(amounts, labels=categories, autopct="%1.1f%%", startangle=90)
    plt.title("Expense Distribution")
    plt.show()
