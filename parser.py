from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import time

# Настройка Selenium
options = Options()
options.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36"
)
options.add_argument("--disable-blink-features=AutomationControlled")

driver = webdriver.Chrome(options=options)


try:
    # Открываем страницу
    driver.get("https://papajohns.ru/yaroslavl")

    # Ждем загрузки секции с пиццами
    pizza_section = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "pizza"))
    )

    # Ищем только внутри этой секции
    product_headers = pizza_section.find_elements(
        By.CSS_SELECTOR, '[class="_2qj-DTg_kGPvRApDKha_-w"]'
    )

    pizza_data = []

    for product in product_headers:
        # Название
        name = product.find_element(
            By.CSS_SELECTOR, '[data-test-id="product_card_header"]'
        ).text

        # Описание
        description = product.find_element(
            By.CSS_SELECTOR, '[class="_2uYmw-6znBwRpeYTuDcvPN"]'
        ).text

        # Извлекаем текст в отдельный список
    pizza_names = [header.text for header in product_headers]

    # Выводим результат
    print("Найдены следующие пиццы в разделе 'Пицца':")
    for name in pizza_names:
        print(f"- {name}")

    # Сохраняем в переменную
    all_pizza_names = pizza_names

except Exception as e:
    print(f"Произошла ошибка: {e}")

finally:
    driver.quit()

# Теперь переменная all_pizza_names содержит только пиццы из нужной секции
print("\nВсе названия из секции 'pizza':")
print(all_pizza_names)
