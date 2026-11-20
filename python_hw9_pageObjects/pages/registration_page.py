from selene import browser, have, be

from utils import path, close_modal


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
        browser.all('#genterWrapper label').element_by(have.exact_text(value)).click()

    def fill_phone(self, value):
        browser.element('#userNumber').type(value)

    def fill_birthday(self, day, month, year):
        browser.element('#dateOfBirthInput').click()

        browser.element('.react-datepicker__month-select').type(month)
        browser.element('.react-datepicker__year-select').type(year)
        browser.element(f'.react-datepicker__day--{day:03}:not(.react-datepicker__day--outside-month)').click()

        browser.element('#dateOfBirthInput').should(have.value(f'{day} {month[0:3]} {year}'))

    def upload_picture(self, value):
        browser.element('#uploadPicture').send_keys(path(value))

    def fill_address(self, value):
        browser.element("#currentAddress").type(value)

    def fill_hobbies(self, *values):
        for value in values:
            browser.all('#hobbiesWrapper label').element_by(have.exact_text(value)).click()

    def fill_subject(self, *values):
        browser.element('#subjectsInput').should(be.blank)
        for value in values:
            browser.element('#subjectsInput').type(value)

            close_modal()

            browser.element('#subjectsInput').press_enter()
            browser.all('.subjects-auto-complete__multi-value__label').should(have.exact_texts(*values))
