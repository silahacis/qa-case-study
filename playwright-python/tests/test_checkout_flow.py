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

def test_checkout_flow(page: Page):
    # 1) Login
    login(page)

    # Ensure inventory page is loaded
    expect(page).to_have_url(BASE_URL + "inventory.html")
    expect(page.locator(".title")).to_have_text("Products")

    # 2) Add first product to cart
    first_item_add_button = page.locator('[data-test="add-to-cart-sauce-labs-backpack"]')
    first_item_add_button.click()

    # Verify cart badge shows 1 item
    cart_badge = page.locator(".shopping_cart_badge")
    expect(cart_badge).to_have_text("1")

    # 3) Go to cart
    page.locator(".shopping_cart_link").click()
    expect(page.locator(".title")).to_have_text("Your Cart")

    # Validate item exists in cart
    cart_item = page.locator(".cart_item")
    expect(cart_item).to_have_count(1)

    # 4) Begin checkout
    page.locator('[data-test="checkout"]').click()
    expect(page.locator(".title")).to_have_text("Checkout: Your Information")

    # 5) Fill checkout info
    page.locator('[data-test="firstName"]').fill("Sila")
    page.locator('[data-test="lastName"]').fill("Hacialioglu")
    page.locator('[data-test="postalCode"]').fill("07000")

    page.locator('[data-test="continue"]').click()

    # 6) Validate checkout overview page
    expect(page.locator(".title")).to_have_text("Checkout: Overview")

    # Item summary visible
    expect(page.locator(".cart_item")).to_have_count(1)

    # Price summary
    expect(page.locator(".summary_subtotal_label")).to_be_visible()
    expect(page.locator(".summary_total_label")).to_be_visible()

    # STOP BEFORE PAYMENT (do NOT click Finish)

def test_basic_accessibility_checks(page: Page):
    # 1) Login
    login(page)

    # Validate inventory loaded
    expect(page).to_have_url(BASE_URL + "inventory.html")

    # --- IMAGE ALT TEXT CHECK ---
    first_image = page.locator("img.inventory_item_img").first
    alt_value = first_image.get_attribute("alt")
    assert alt_value is not None and alt_value.strip() != "", "Image has missing alt text"

    # --- CHECK BUTTON ACCESSIBILITY ROLES ---
    add_button = page.locator('[data-test="add-to-cart-sauce-labs-backpack"]')
    role = add_button.get_attribute("role")

    # Playwright exposes ARIA metadata; buttons often have implicit role
    assert role in (None, "button"), "Add to cart button should have button role"

    # --- CHECK PAGE TITLE IS ACCESSIBLE ---
    page_title = page.locator(".title")
    expect(page_title).to_be_visible()
    assert page_title.inner_text().strip() == "Products"
