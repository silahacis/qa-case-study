import pytest
from playwright.sync_api import sync_playwright

@pytest.fixture(scope="session")
def playwright_instance():
    with sync_playwright() as p:
        yield p

@pytest.fixture(scope="session")
def browser(playwright_instance):
    browser = playwright_instance.chromium.launch(headless=True)
    yield browser
    browser.close()

@pytest.fixture(scope="function")
def page(browser, request):
    context = browser.new_context()
    page = context.new_page()

    yield page

    # If test fails → take screenshot (flake resistance)
    if request.node.rep_call.failed:
        page.screenshot(path=f"screenshot_{request.node.name}.png")

    context.close()

# Capture test result
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item):
    outcome = yield
    result = outcome.get_result()
    setattr(item, f"rep_{result.when}", result)
