import pandas as pd
import math
from pathlib import Path
from PizzaData import PizzaDataParser


class PizzaDataAnalyzer(PizzaDataParser):
    """
    Класс-наследник PizzaDataParser с добавлением функциональности расчета площади.
    """

    def __init__(self, file_path: str | Path):
        """
        Инициализация анализатора пиццы.
        Args:
            file_path: Путь к JSON-файлу с данными о пиццах
        """
        super().__init__(file_path)
        self._area_calculated = False

    def calculate_area(self):
        """Приватный метод для расчета площади пицц."""
        if self.df is None:
            raise ValueError("Отсутствуют данные для расчёта площади")

        if "size" not in self.df.columns:
            raise ValueError("Отсутствует столбец 'size' ")

        self.df["area"] = self.df["size"].apply(
            lambda diameter: round(math.pi * (diameter / 2) ** 2, 2)
        )
        self._area_calculated = True

        cols = [col for col in self.df.columns if col != "area"] + ["area"]
        self.df = self.df[cols]

    def calculate_price_square_cm(self):
        """Приватный метод для расчета цена за 1 см квадратный."""
        if self.df is None:
            raise ValueError("Отсутствуют данные для расчёта (DataFrame не создан)")

        if "price" not in self.df.columns:
            raise ValueError("Отсутствует столбец 'price'")

        if "area" not in self.df.columns:
            raise ValueError(
                "Сначала нужно рассчитать площадь (вызовите calculate_area())"
            )

        # Рассчитываем цену за см² с округлением до 2 знаков
        self.df["price_cm"] = round(self.df["price"] / self.df["area"], 2)

        # Перемещаем новый столбец в конец
        cols = [col for col in self.df.columns if col != "price_cm"] + ["price_cm"]
        self.df = self.df[cols]

    def filter_by_price_cm(
        self, min_price: float = None, max_price: float = None
    ) -> pd.DataFrame:
        """
        Фильтрует пиццы по цене за см²
        Args:
            min_price: Минимальная цена за см²
            max_price: Максимальная цена за см²
        Returns:
            Отфильтрованный DataFrame
        """
        if "price_cm" not in self.df.columns:
            raise ValueError(
                "Сначала рассчитайте price_cm (вызовите calculate_price_square_cm())"
            )

        mask = True
        if min_price is not None:
            mask = mask & (self.df["price_cm"] >= min_price)
        if max_price is not None:
            mask = mask & (self.df["price_cm"] <= max_price)

        return self.df[mask].copy()

    def get_best_bargains(self, n: int = 3) -> pd.DataFrame:
        """Возвращает n самых выгодных пицц"""
        return self.df.nsmallest(n, "price_cm")


pizza = PizzaDataAnalyzer("data/pizzas.json")
pizza.to_dataframe()
pizza.calculate_area()
pizza.calculate_price_square_cm()
pizza.print_random_sample()

print("Самые выгодные пиццы:")
print(pizza.get_best_bargains(3))


print("\nПиццы в ценовом диапазоне 1.5-2 руб/см²:")
print(pizza.filter_by_price_cm(min_price=1.5, max_price=2))

# Сортировка по цене за см²
sorted_by_value = pizza.df.sort_values("price_cm")
print("\nВсе пиццы отсортированные по выгодности:")
print(sorted_by_value[["name", "price_cm"]])
