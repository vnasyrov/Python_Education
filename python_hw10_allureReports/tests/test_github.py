from selene import browser, by, be, have


def test_github():
    browser.open("https://github.com")

    browser.element('[aria-label="Search or jump to, type / to search"]').click()
    browser.element('[aria-label="Search or jump to"]').type("vnasyrov/Python_Education")
    browser.element('[aria-label="Search or jump to"]').press_enter()

    browser.element(by.link_text("vnasyrov/Python_Education")).click()
    browser.element('[data-tab-item="issues"]').click()

    browser.element('[data-testid="issue-listitem-title-link"]').should(have.text("Тестовый Issue"))
