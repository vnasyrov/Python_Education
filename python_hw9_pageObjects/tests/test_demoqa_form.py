from datetime import datetime

from selene import browser, have, be, command

from pages.registration_page import RegistrationPage
from utils import close_modal, path


def test_demoqa_form():
    registration_page = RegistrationPage()  # создали объект страницы
    registration_page.open()  # нажали выключатель

    # Убираем баннер и футер, мешающие кнопке Submit
    browser.driver.execute_script("document.querySelector('footer').remove()")

    # Основные поля
    registration_page.fill_first_name('Valeriy')
    registration_page.fill_last_name('Nasyrov')
    registration_page.fill_email('user@example.com')
    registration_page.fill_gender('Male')
    registration_page.fill_phone('9999999999')

    # Дата рождения
    today = datetime.today().strftime('%d %b %Y')
    browser.element('#dateOfBirthInput').should(have.value(today))

    registration_page.fill_birthday(12, 'July',1993)

    # Subjects
    registration_page.fill_subject('Maths')

    #     browser.element('.subjects-auto-complete__multi-value__label').should(have.text('Maths'))
    #     browser.element('.subjects-auto-complete__multi-value__remove').click()
    #     browser.element('#subjectsInput').should(be.blank)
    #     browser.element('#subjectsInput').type('Maths')
    #     close_modal()
    #     browser.element('#subjectsInput').press_enter()

    # .modal-content
    # #closeLargeModal

    #Hobbies
    registration_page.fill_hobbies('Sports', 'Reading', 'Music')

    # Picture
    registration_page.upload_picture('1.jpg')

    # Current Address
    registration_page.fill_address('Los Angeles')

    # State
    browser.element('#react-select-3-placeholder').should(have.text('Select State'))
    browser.element('#react-select-3-input').should(be.clickable)
    browser.element('#react-select-3-input').should(have.no.attribute('aria-controls', 'react-select-3-listbox'))
    browser.element('#react-select-3-input').click()
    browser.element('#react-select-3-listbox').should(be.visible)
    browser.element('#react-select-3-listbox').all('[role="option"]'
                    ).should(have.exact_texts('NCR', 'Uttar Pradesh', 'Haryana', 'Rajasthan'))
    browser.element('#react-select-4-input').should(have.js_property('disabled', True)) # проверяем что выбор города недоступен до выбора страны
    browser.element('#react-select-3-input').type('Uttar Pradesh').press_enter()
    browser.element('#react-select-3-listbox').should(be.not_.visible)

    # City
    browser.element('#react-select-4-placeholder').should(have.text('Select City'))
    browser.element('#react-select-4-input').should(be.clickable)
    browser.element('#react-select-4-input').should(have.no.attribute('aria-controls', 'react-select-4-listbox'))
    browser.element('#react-select-4-input').click()
    browser.element('#react-select-4-listbox').should(be.visible)
    browser.element('#react-select-4-listbox').all('[role="option"]'
                    ).should(have.exact_texts('Agra', 'Lucknow', 'Merrut'))
    browser.element('#react-select-4-input').type('Agra').press_enter()
    browser.element('#react-select-4-listbox').should(be.not_.visible)

    # Submit
    browser.element('#submit').perform(command.js.click)
    browser.element('.table-responsive').should(be.visible)
    browser.element('#example-modal-sizes-title-lg').should(have.exact_text('Thanks for submitting the form'))
    browser.all('.table-responsive td:nth-child(2)').should(have.exact_texts(

        'Valeriy Nasyrov',
        'user@example.com',
        'Male',
        '9999999999',
        '12 July,1993',
        'Maths',
        'Sports, Reading, Music',
        '1.jpg',
        'Los Angeles',
        'Uttar Pradesh Agra'
    ))