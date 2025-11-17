from playwright.sync_api import Page, expect

BASE_URL = "https://www.saucedemo.com/"

def test_login_success(page: Page):
    page.goto(BASE_URL)

    page.locator('[data-test="username"]').fill("standard_user")
    page.locator('[data-test="password"]').fill("secret_sauce")
    page.locator('[data-test="login-button"]').click()

    expect(page).to_have_url(BASE_URL + "inventory.html")
    expect(page.locator(".title")).to_have_text("Products")

def test_login_invalid_credentials(page: Page):
    page.goto(BASE_URL)
    page.locator('[data-test="username"]').fill("invalid_user")
    page.locator('[data-test="password"]').fill("wrong_password")
    page.locator('[data-test="login-button"]').click()

    error_msg = page.locator('[data-test="error"]')
    expect(error_msg).to_be_visible()
    expect(error_msg).to_contain_text("Username and password do not match")

def test_login_locked_out_user(page: Page):
    page.goto(BASE_URL)

    page.locator('[data-test="username"]').fill("locked_out_user")
    page.locator('[data-test="password"]').fill("secret_sauce")
    page.locator('[data-test="login-button"]').click()

    expect(page.locator('[data-test="error"]')).to_have_text("Epic sadface: Sorry, this user has been locked out.")
