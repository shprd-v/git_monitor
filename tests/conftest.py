import pytest
from playwright.sync_api import sync_playwright, Browser, Page
from pathlib import Path
from datetime import datetime


@pytest.fixture(scope="session")
def browser() -> Browser:
    print("Запуск браузера...")
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=False,
            slow_mo=500
        )
        yield browser
        print("Закрытие браузера...")
        browser.close()


@pytest.fixture(scope="function")
def page(browser) -> Page:
    context = browser.new_context(
        viewport={'width': 1920, 'height': 1080}
    )
    page = context.new_page()
    yield page
    page.close()
    context.close()


@pytest.fixture
def login_page(page):
    from pages.login_page import LoginPage
    return LoginPage(page)


@pytest.fixture
def valid_user():
    return {
        "username": "standard_user",
        "password": "secret_sauce"
    }


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    
    if rep.when == "call" and rep.failed:
        page = item.funcargs.get("page")
        if page:
            screenshot_dir = Path("screenshots")
            screenshot_dir.mkdir(exist_ok=True)
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            screenshot_path = screenshot_dir / f"{item.name}_{timestamp}.png"
            
            page.screenshot(path=str(screenshot_path))
            print(f"Скриншот ошибки: {screenshot_path}")
