import pytest
import re  # Импортирование модуля для работы с регулярными выражениями Python RegEx
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def test_all_my_pets_present():
    """Тест для проверки страницы со списком питомцев пользователя на присутствие всех питомцев."""

    # Неявное ожидание.
    pytest.driver.implicitly_wait(10)

# Первый вариант.

    # # Подсчет карточек моих питомцев
    # number_of_pets = pytest.driver.find_elements(By.CSS_SELECTOR, '.table tbody tr')
    # # Блок статистики с моими питомцами
    # stat_of_pets = pytest.driver.find_element(By.CSS_SELECTOR, '.\\.col-sm-4.left')

    # pattern = r'Питомцев: (\d+)'                    # Сырая строка из статистики по моим питомцам, \d+ - число моих питомцев
    # result = re.search(pattern, stat_of_pets.text)  # Результат поиска строки в блоке статистики, применен модуль регулярных выражений
    # amount_of_pets = int(result.group(1))           # Метод group применен для второй части (\d+) строчки pattern, где отображено число моих питомцев
    #                                                 # group() – возвращает фрагмент строки, в котором было обнаружено совпадение.
    # # Сравнение результатов
    # assert len(number_of_pets) == amount_of_pets, "Не все питомцы присутствуют на моей странице."

# Второй вариант.

    # Извлечение числа моих питомцев из блока статистики.
    pets_number = pytest.driver.find_element(By.XPATH, '//div[@class=".col-sm-4 left"]').text.split('\n')[1].split(' ')[1]
    # Подсчет карточек моих питомцев
    pets_count = pytest.driver.find_elements(By.XPATH, '//table[@class="table table-hover"]/tbody/tr')
    # Сравнение результатов
    assert int(pets_number) == len(pets_count), "Не все питомцы присутствуют на моей странице."


def test_half_of_my_pets_have_photo():
    """Тест для проверки наличия фотографий хотя бы у половины питомцев."""

    # Явное ожидание.
    element = WebDriverWait(pytest.driver, 10).until(
        EC.presence_of_element_located((By.ID, "all_my_pets"))
    )

    # Список моих питомцев из таблицы
    pets = element.find_elements(By.CSS_SELECTOR, 'tbody tr')

    # Подсчет количества питомцев с фото
    pets_with_photo = 0

    for pet in pets:
        photo = pet.find_element(By.TAG_NAME, 'img').get_attribute('src')
        if photo:
            pets_with_photo += 1

    assert pets_with_photo >= len(pets)/2, "Более чем у половины моих питомцев нет фотографий."


def test_all_my_pets_have_name_age_breed():
    """Тест для проверки наличия имени, возраста и породы у моих питомцев."""

    # Явное ожидание.
    element = WebDriverWait(pytest.driver, 10).until(
        EC.presence_of_element_located((By.ID, "all_my_pets"))
    )

    # Список моих питомцев из таблицы
    pets = element.find_elements(By.CSS_SELECTOR, 'tbody tr')

    for pet in pets:
        data = pet.find_elements(By.CSS_SELECTOR, 'tbody tr td')
        assert data[0].text, "У питомца отсутствует имя."
        assert data[1].text, "У питомца отсутствует порода."
        assert data[2].text, "У питомца отсутствует возраст."


def test_all_my_pets_have_different_names():
    """Тест для проверки, что у всех питомцев разные имена."""

    # Неявное ожидание.
    pytest.driver.implicitly_wait(10)

    # Список имен всех моих питомцев
    pet_names = pytest.driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table/tbody/tr/td[1]')

    # Проверяем уникальность имен
    names = []

    for pet_name in pet_names:
        name = pet_name.text.strip()  # strip() возвращает копию строки, при этом удаляя как начальные, так и конечные символы.
        if name in names:
            pytest.fail(f"Повторяющееся имя питомца: {name}")
        names.append(name)


def test_all_my_pets_are_different():
    """Тест для проверки отсутствия повторяющихся питомцев."""

    # Неявное ожидание.
    pytest.driver.implicitly_wait(10)

    # Список моих питомцев из таблицы
    pets_table = pytest.driver.find_elements(By.XPATH, "//tbody/tr")

    pets = []

    for i in pets_table:
        # Извлекаем значение имени, породы и возраста из каждой строки таблицы
        pet_name = i.find_element(By.XPATH, './td[1]').text.strip()
        pet_breed = i.find_element(By.XPATH, './td[2]').text.strip()
        pet_age = i.find_element(By.XPATH, './td[3]').text.strip()

        # Создаем кортеж с именем, породой и возрастом
        pet = (pet_name, pet_breed, pet_age)

        # Поиск одинаковых питомцев
        if pet in pets:
            pytest.fail(f"Найден дублирующийся питомец: {pet}")
        pets.append(pet)
