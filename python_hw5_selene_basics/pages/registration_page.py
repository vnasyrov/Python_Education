from selene import browser, have, be, command
from utils import close_modal, path


class RegistrationPage:
    def open(self):
        browser.open('/automation-practice-form')

    def fill_first_name(self, value):
        browser.element('#firstName').type(value)

    def fill_last_name(self, value):
        browser.element('#lastName').type(value)

    def fill_email(self, value):
        browser.element('#userEmail').type(value)

    def fill_gender(self, value):
        # Ищем label внутри блока пола и кликаем по тому, где текст совпадает
        browser.all('#genterWrapper label').element_by(have.exact_text(value)).click()

    def fill_phone(self, value):
        browser.element('#userNumber').type(value)

    def fill_birthday(self, day, month, year):
        # 1. Открываем календарь
        browser.element('#dateOfBirthInput').click()

        # 2. Выбираем месяц и год
        browser.element('.react-datepicker__month-select').type(month)
        browser.element('.react-datepicker__year-select').type(year)

        # 3. Кликаем по дню (с защитой от дней из соседних месяцев)
        # {day:03} делает из 5 -> 005, из 12 -> 012
        browser.element(f'.react-datepicker__day--{day:03}:not(.react-datepicker__day--outside-month)').click()

        # 4. Проверяем, что дата установилась верно
        expected_text = f'{day} {month[:3]} {year}'
        browser.element('#dateOfBirthInput').should(have.value(expected_text))

    def upload_picture(self, filename):
        browser.element('#uploadPicture').send_keys(path(filename))

    def fill_address(self, value):
        browser.element('#currentAddress').type(value)

    def fill_hobbies(self, *values):
        for value in values:
            # Находим нужный label по тексту и кликаем
            browser.all('#hobbiesWrapper label').element_by(have.exact_text(value)).click()

    def fill_subject(self, *values):
        browser.element('#subjectsInput').should(be.blank)

        for value in values:
            browser.element('#subjectsInput').type(value)
            close_modal()
            browser.element('#subjectsInput').press_enter()

        # Проверяем, что все предметы появились в списке
        browser.all('.subjects-auto-complete__multi-value__label').should(have.exact_texts(*values))

    def fill_state(self, value):
        browser.element('#react-select-3-input').type(value).press_enter()
