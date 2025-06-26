import math


class Menu:
    def __init__(self):
        self.menu = []

    def add_pizza(self, pizza):
        self.menu.append(pizza)


class Pizza:
    def __init__(self, name: str, diameter: int, price: int, menu: Menu):
        self.name = name
        self.diameter = diameter
        self.price = price
        menu.add_pizza(self)

    def calculate_area(self, cut: int = 0):
        radius = self.diameter / 2 - cut
        area = math.pi * (radius**2)
        return round(area, 2)

    def calculate_profit(self, cut: int = 0):
        profit = self.price / self.calculate_area(cut=cut)
        return round(profit, 2)

    def __str__(self):
        return (
            f"{self.name:<20} | {self.diameter:>5} см | {self.price:>6} руб | "
            f"{self.calculate_area():>7.2f} ({self.calculate_area(cut=2):>7.2f}) см² | {self.calculate_profit():>5.2f} ({self.calculate_profit(cut=2):>4.2f}) руб/см²"
        )


# Создаем меню
menu = Menu()

# Создаем пиццы и добавляем их в меню
pizza1 = Pizza(name="Пепперони грин", diameter=30, price=615, menu=menu)
pizza2 = Pizza(name="Пепперони грин", diameter=35, price=779, menu=menu)
pizza3 = Pizza(name="Пепперони грин", diameter=40, price=919, menu=menu)
pizza4 = Pizza(name="Ветчина и бекон", diameter=30, price=695, menu=menu)
pizza5 = Pizza(name="Ветчина и бекон", diameter=35, price=869, menu=menu)
pizza6 = Pizza(name="Ветчина и бекон", diameter=40, price=989, menu=menu)

# Выводим все пиццы из меню
print("\nВсе пиццы в меню:")
for pizza in menu.menu:
    print(pizza)
