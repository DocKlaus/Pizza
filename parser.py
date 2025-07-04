from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
import json
from pathlib import Path
import logging

# Настройка логирования
logging.basicConfig(
    level=logging.ERROR,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()],
)

logger = logging.getLogger(__name__)


# Настройка Selenium
options = Options()
options.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36"
)
options.add_argument("--disable-blink-features=AutomationControlled")

driver = webdriver.Chrome(options=options)
actions = ActionChains(driver)


def get_text(source, attribute, value):
    result = source.find_element(By.CSS_SELECTOR, f"[{attribute}={value}]").text
    return result


def get_object(
    source, attribute, value: str = "", get_list: bool = False
) -> list | str:

    arg = f"[{attribute}={value}]"

    if not get_list:
        result = source.find_element(By.CSS_SELECTOR, arg)
        return result
    else:
        result = source.find_elements(By.CSS_SELECTOR, arg)
        return result


try:
    # Открываем страницу
    driver.get("https://papajohns.ru/yaroslavl")

    # Ждем загрузки секции с пиццами
    pizza_section = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "pizza"))
    )

    # Ищем только внутри этой секции
    product_headers = get_object(
        source=pizza_section,
        attribute="class",
        value="_2qj-DTg_kGPvRApDKha_-w",
        get_list=True,
    )
    logger.debug(f"product_headers: {len(product_headers)}")

    pizza_data = []

    for product in product_headers:
        actions.move_to_element(product).perform()

        # Поиск кнопок выбора теста
        dough_buttons = get_object(
            source=product,
            attribute="class*",
            value="_22tLg_N-T1_fSuHivc553F",
            get_list=True,
        )
        logger.debug(f"dough_buttons: {len(dough_buttons)}")
        logger.debug(
            f"text button 1: {dough_buttons[0].text} text button 2: {dough_buttons[1].text}"
        )

        crust = None

        # Проверяем кнопки
        for button in dough_buttons:
            actions.move_to_element(button).perform()
            class_attribute = button.get_attribute("class")

            # Если кнопка уже активна (содержит gFWUICI_xCcypOmIgwq3L)
            if "gFWUICI_xCcypOmIgwq3L" in class_attribute:
                crust = button.text
                logger.debug(f"crust: {crust}")

            else:
                # Нажимаем на неактивную кнопку (например, "Тонкое")
                button.click()
                # time.sleep(1)

                # Проверяем, что кнопка стала активной
                updated_class = button.get_attribute("class")
                if "gFWUICI_xCcypOmIgwq3L" in updated_class:
                    crust = button.text
                    logger.debug(f"crust: {crust}")

            # Здесь же надо найти диаметр и цену

            # Находим блок с кнопками размеров
            size_selector = get_object(
                source=product, attribute="data-test-id", value="size_selector"
            )
            logger.debug(f"size_selector: {size_selector}")

            # список кнопок в этом блоке
            size_buttons = get_object(
                source=size_selector,
                attribute="class*",
                value="AkOaPdzKXXkN8Vsguj3lh",
                get_list=True,
            )
            logger.debug(f"size_buttons: {len(size_buttons)}")

            # Кликабельность кнопок
            for size_button in size_buttons:
                dict = {}
                actions.move_to_element(size_button).perform()
                size_button_attribute = size_button.get_attribute("class")

                if "_3ZxcheiXBqcNXPHFDFBcmo" in size_button_attribute:
                    diameter = int(size_button.text.replace("см", "").strip())
                    logger.debug(f"size: {diameter}")

                else:

                    size_button.click()
                    # time.sleep(1)
                    updated_size_b_attribute = size_button.get_attribute("class")
                    if "_3ZxcheiXBqcNXPHFDFBcmo" in updated_size_b_attribute:
                        diameter = int(size_button.text.replace("см", "").strip())
                        logger.debug(f"size: {diameter}")

                dict["name"] = get_text(
                    source=product,
                    attribute="data-test-id",
                    value="product_card_header",
                )
                dict["description"] = get_text(
                    source=product, attribute="class", value="_2uYmw-6znBwRpeYTuDcvPN"
                )
                dict["crust"] = crust
                dict["size"] = diameter
                dict["price"] = int(
                    get_text(
                        source=product, attribute="data-test-id", value="amount_price"
                    )
                    .replace(" ₽", "")
                    .replace(" ", "")
                )
                pizza_data.append(dict)


except Exception as e:
    print(f"Произошла ошибка: {e}")

finally:
    driver.quit()

try:
    # Создаем директорию, если её нет
    Path("data").mkdir(exist_ok=True)

    # Сохраняем с красивым форматированием
    with open("data/pizzas.json", "w", encoding="utf-8") as f:
        json.dump(
            pizza_data,
            f,
            ensure_ascii=False,  # Для корректного отображения кириллицы
            indent=2,  # Отступы для читаемости
        )

    print("Данные успешно сохранены в data/pizzas.json")
except Exception as e:
    print(f"Ошибка при сохранении: {e}")
