import math
import pandas as pd


class PizzaBuilder:
    def __init__(self, menu):
        self.menu = menu

    def add(self, name, diameter, price):
        Pizza(
            name=name,
            diameter=diameter,
            price=price,
            menu=self.menu,
        )
        return self


class Menu:
    def __init__(self):
        self.menu = []
        self.df = pd.DataFrame(
            columns=[
                "Название",
                "Диаметр (см)",
                "Цена (руб)",
                "Площадь (см²)",
                "Площадь без бортика (см²)",
                "Отношение (руб/см²)",
                "Отношение без бортика (руб/см²)",
            ]
        )

    def add_pizza(self, pizza):
        self.menu.append(pizza)
        new_row = {
            "Название": pizza.name,
            "Диаметр (см)": pizza.diameter,
            "Цена (руб)": pizza.price,
            "Площадь (см²)": pizza.calculate_area(),
            "Площадь без бортика (см²)": pizza.calculate_area(cut=2),
            "Отношение (руб/см²)": pizza.calculate_profit(),
            "Отношение без бортика (руб/см²)": pizza.calculate_profit(cut=2),
        }
        self.df = pd.concat([self.df, pd.DataFrame([new_row])], ignore_index=True)

    def show_menu(self):
        print("\nМеню в виде таблицы Pandas:")
        print(self.df.to_string(index=False))

    def get_most_profitable(self, with_rim=True):
        column = (
            "Отношение (руб/см²)" if with_rim else "Отношение без бортика (руб/см²)"
        )
        return self.df.loc[self.df[column].idxmax()]


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
builder = PizzaBuilder(menu)
(
    builder.add("Пепперони грин", 30, 615)
    .add("Пепперони грин", 35, 779)
    .add("Пепперони грин", 40, 919)
    .add("Ветчина и бекон", 30, 695)
    .add("Ветчина и бекон", 35, 869)
    .add("Ветчина и бекон", 40, 989)
)

# Выводим меню в виде таблицы Pandas
menu.show_menu()

# Анализ данных
print("\nСамая выгодная пицца (с бортиком):")
print(menu.get_most_profitable(with_rim=True))

print("\nСамая выгодная пицца (без бортика):")
print(menu.get_most_profitable(with_rim=False))


# Дополнительный анализ
print("\nСредняя цена пицц:", round(menu.df["Цена (руб)"].mean(), 2), "руб")
print("Сортировка по отношению:")
print(menu.df.sort_values("Отношение (руб/см²)").to_string(index=False))
