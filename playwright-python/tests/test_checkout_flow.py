from playwright.sync_api import Page, expect

BASE_URL = "https://www.saucedemo.com/"

def login(page: Page, username="standard_user", password="secret_sauce"):
    page.goto(BASE_URL)
    page.locator('[data-test="username"]').fill(username)
    page.locator('[data-test="password"]').fill(password)
    page.locator('[data-test="login-button"]').click()

def test_inventory_listing_and_product_detail(page: Page):
    # Login
    login(page)

    # Validate we are on inventory page
    expect(page).to_have_url(BASE_URL + "inventory.html")
    expect(page.locator(".title")).to_have_text("Products")

    # 1) Inventory list should contain 6 products
    products = page.locator(".inventory_item")
    expect(products).to_have_count(6)

    # 2) Validate first product has required elements
    first_item = products.nth(0)
    expect(first_item.locator(".inventory_item_name")).to_be_visible()
    expect(first_item.locator(".inventory_item_desc")).to_be_visible()
    expect(first_item.locator(".inventory_item_price")).to_be_visible()

    # 3) Click first product to go to product detail page
    first_item.locator(".inventory_item_name").click()

    # 4) Validate product detail page is opened
    expect(page.locator(".inventory_details_name")).to_be_visible()
    expect(page.locator(".inventory_details_desc")).to_be_visible()
    expect(page.locator(".inventory_details_price")).to_be_visible()

    # Optional: back button visible
    expect(page.locator('[data-test="back-to-products"]')).to_be_visible()
