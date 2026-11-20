from selene import browser, have, be, commaЫnd

from pages.registration_page import RegistrationPage


def test_demoqa_form():
    registration_page = RegistrationPage()
    registration_page.open()

    # Убираем баннер и футер, мешающие кнопке Submit
    browser.driver.execute_script("document.querySelector('footer').remove()")

    # Основные поля
    registration_page.fill_first_name('Valeriy')
    registration_page.fill_last_name('Nasyrov')
    registration_page.fill_email('user@example.com')
    registration_page.fill_gender('Male')
    registration_page.fill_phone('9999999999')

    # Дата рождения
    registration_page.fill_birthday(12, 'July', 1993)

    # Subjects
    registration_page.fill_subject('Maths')

    #Hobbies
    registration_page.fill_hobbies('Sports', 'Reading', 'Music')

    # Picture
    registration_page.upload_picture('1.jpg')

    # Current Address
    registration_page.fill_address('Los Angeles')

    # State
    registration_page.fill_state('Uttar Pradesh')

    # City
    registration_page.fill_city('Agra')

    # Submit
    registration_page.submit()
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