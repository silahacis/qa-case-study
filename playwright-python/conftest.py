import os
import pytest
from playwright.sync_api import sync_playwright

# Ensure screenshots directory exists
SCREENSHOT_DIR = "screenshots"
os.makedirs(SCREENSHOT_DIR, exist_ok=True)


@pytest.fixture(scope="session")
def playwright_instance():
    with sync_playwright() as p:
        yield p

@pytest.fixture(scope="session")
def browser(playwright_instance):
    browser = playwright_instance.chromium.launch(headless=False)
    yield browser
    browser.close()

@pytest.fixture(scope="function")
def page(browser, request):
    context = browser.new_context()
    page = context.new_page()

    yield page

    # If test fails → take screenshot (flake resistance)
    if hasattr(request.node, "rep_call") and request.node.rep_call.failed:
        file_path = os.path.join(
            SCREENSHOT_DIR,
            f"{request.node.name}.png"
        )
        page.screenshot(path=file_path)
        print(f"\n📸 Screenshot saved: {file_path}")

    context.close()

# Capture test result
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item):
    outcome = yield
    result = outcome.get_result()
    setattr(item, f"rep_{result.when}", result)
