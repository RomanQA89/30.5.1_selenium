import pytest
from selenium import webdriver
from settings import driver_path, valid_email, valid_password
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.fixture(autouse=True)
def testing():
    pytest.driver = webdriver.Chrome(driver_path)

    # Переходим на страницу авторизации
    pytest.driver.maximize_window()
    pytest.driver.get('http://petfriends.skillfactory.ru/login')

    # Вводим email
    WebDriverWait(pytest.driver, 10).until(
        EC.presence_of_element_located((By.ID, 'email'))
    )
    pytest.driver.find_element(By.ID, 'email').send_keys(valid_email)

    # Вводим пароль
    WebDriverWait(pytest.driver, 10).until(
        EC.presence_of_element_located((By.ID, 'pass'))
    )
    pytest.driver.find_element(By.ID, 'pass').send_keys(valid_password)

    # Нажимаем на кнопку входа в аккаунт
    WebDriverWait(pytest.driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'button[type="submit"]'))
    )
    pytest.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()

    # Проверяем, что мы оказались на главной странице пользователя
    WebDriverWait(pytest.driver, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, 'h1'))
    )
    assert pytest.driver.find_element(By.TAG_NAME, 'h1').text == "PetFriends"

    # Нажимаем на кнопку "Мои питомцы"
    WebDriverWait(pytest.driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="navbarNav"]/ul[1]/li[1]/a[1]'))
    )
    pytest.driver.find_element(By.XPATH, '//*[@id="navbarNav"]/ul[1]/li[1]/a[1]').click()

    # Проверяем, что находимся на странице пользователя
    assert pytest.driver.current_url == 'https://petfriends.skillfactory.ru/my_pets'

    yield

    pytest.driver.quit()
