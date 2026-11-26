import allure
from selene import browser, by, be, have


def test_github_steps():
    with allure.step("Открываем главную страницу GitHub"):
        browser.open("https://github.com")

    with allure.step("Находим строку поиска"):
        browser.element('[aria-label="Search or jump to, type / to search"]').click()

    with allure.step("Вводим название репозитория в строку поиска"):
        browser.element('[aria-label="Search or jump to"]').type("vnasyrov/Python_Education")

    with allure.step("Жмем Enter в строке поиска"):
        browser.element('[aria-label="Search or jump to"]').press_enter()

    with allure.step("Переходим по ссылке репозитория"):
        browser.element(by.link_text("vnasyrov/Python_Education")).click()

    with allure.step("Открываем таб Issues"):
        browser.element('[data-tab-item="issues"]').click()

    with allure.step("Проверяем наличие нужного текста в Issue"):
        browser.element('[data-testid="issue-listitem-title-link"]').should(have.text("Тестовый Issue"))
