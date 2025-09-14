class Category:
    def __init__(self, name):
        self.name = name


class Expense:
    def __init__(self, category, description, amount):
        self.category = category
        self.description = description
        self.amount = amount
