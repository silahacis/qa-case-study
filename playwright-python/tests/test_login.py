from playwright.sync_api import Page, expect

BASE_URL = "https://www.saucedemo.com/"

def test_login_success(page: Page):
    page.goto(BASE_URL)

    page.locator('[data-test="username"]').fill("standard_user")
    page.locator('[data-test="password"]').fill("secret_sauce")
    page.locator('[data-test="login-button"]').click()

    expect(page).to_have_url(BASE_URL + "inventory.html")
    expect(page.locator(".title")).to_have_text("Products")