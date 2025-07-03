import json
import pandas as pd
from pathlib import Path
import random


class PizzaDataParser:
    """
    Класс для парсинга данных о пиццах из JSON-файла.
    Гарантирует порядок колонок: name, crust, size, price, description.
    """

    def __init__(self, file_path: str | Path):
        self.file_path = Path(file_path)
        if not self.file_path.exists():
            raise FileNotFoundError(f"Файл не найден: {self.file_path}")
        self.data = None
        self.df = None

    def parse(self):
        """Читает и парсит JSON-файл."""
        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                self.data = json.load(f)

            if not isinstance(self.data, list):
                raise ValueError("JSON должен содержать список пицц")

        except json.JSONDecodeError as e:
            raise ValueError(f"Ошибка парсинга JSON: {e}")
        return self

    def _reorder_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        """Упорядочивает колонки: name, crust, size, price"""
        preferred_order = ["name", "crust", "size", "price"]
        existing_columns = [col for col in preferred_order if col in df.columns]
        return df[existing_columns]

    def to_dataframe(self) -> pd.DataFrame:
        """Конвертирует данные в DataFrame с заданным порядком колонок."""
        if self.data is None:
            self.parse()

        self.df = pd.DataFrame(self.data)

        # Валидация обязательных полей
        required_fields = {"name", "crust", "size", "price"}
        if not required_fields.issubset(self.df.columns):
            missing = required_fields - set(self.df.columns)
            raise ValueError(f"Отсутствуют обязательные поля: {missing}")

        # Упорядочиваем колонки
        self.df = self._reorder_columns(self.df)

        return self.df

    def print_random_sample(self, n: int = 5, desc_length: int = 10):
        """
        Выводит образец данных в консоль в заданном формате без столбца description.

        Args:
            n: Количество строк для вывода
            desc_length: Длина описания (символов)
        """
        if self.df is None or len(self.df) == 0:
            raise ValueError("Нет данных для отображения")

        sample_size = min(n, len(self.df))

        df_sample = self.df.sample(sample_size).copy()

        # Удаляем столбец description, если он есть
        if "description" in df_sample.columns:
            df_sample = df_sample.drop(columns=["description"])

        # Настраиваем отображение
        pd.set_option("display.max_columns", None)
        pd.set_option("display.width", None)
        pd.set_option("display.max_colwidth", 20)

        # Выводим результат
        print(f"\nСлучайные {sample_size} пицц из меню:")
        print(df_sample.to_string(index=False))
        print(f"\nВсего пицц в меню: {len(self.df)}")


# pizza = PizzaDataParser("data/pizzas.json")
# pizza.parse()
# pizza.to_dataframe()
# pizza.print_random_sample()
