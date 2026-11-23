from pages.registration_page import RegistrationPage


def test_demoqa_form():
    registration_page = RegistrationPage()
    registration_page.open()

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
    registration_page.should_have_registered(
        full_name='Valeriy Nasyrov',
        email='user@example.com',
        gender='Male',
        phone='9999999999',
        birthday='12 July,1993',
        subjects='Maths',
        hobbies='Sports, Reading, Music',
        picture='1.jpg',
        current_address='Los Angeles',
        state_city='Uttar Pradesh Agra'
    )