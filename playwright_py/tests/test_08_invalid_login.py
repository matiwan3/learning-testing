import re

import pytest
from playwright.sync_api import Page, expect

# Practice site made for automation: https://the-internet.herokuapp.com/login


@pytest.fixture(autouse=True)
def open_login_page(page: Page):
    # equivalent of test.beforeEach in TypeScript
    page.goto("https://the-internet.herokuapp.com/login")


def test_wrong_password_shows_an_error_message(page: Page):
    page.get_by_label("Username").fill("tomsmith")
    page.get_by_label("Password").fill("wrong-password")
    page.get_by_role("button", name="Login").click()

    flash = page.locator("#flash")
    expect(flash).to_be_visible()
    expect(flash).to_contain_text("Your password is invalid!")
    expect(page).to_have_url(re.compile(r"/login$"))  # still on the login page


def test_wrong_username_shows_a_different_error(page: Page):
    page.get_by_label("Username").fill("nobody")
    page.get_by_label("Password").fill("SuperSecretPassword!")
    page.get_by_role("button", name="Login").click()

    expect(page.locator("#flash")).to_contain_text("Your username is invalid!")


def test_correct_credentials_log_in(page: Page):
    page.get_by_label("Username").fill("tomsmith")
    page.get_by_label("Password").fill("SuperSecretPassword!")
    page.get_by_role("button", name="Login").click()

    expect(page).to_have_url(re.compile(r"/secure$"))
    expect(page.locator("#flash")).to_contain_text("You logged into a secure area!")
