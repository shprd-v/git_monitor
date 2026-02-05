"""
Скрипт создания полной структуры Playwright проекта
"""

from pathlib import Path


def create_project_structure():
    """Создать полную структуру проекта с заполненными файлами"""
    
    print("🚀 Создание структуры Playwright проекта...\n")
    
    # ============== СОЗДАНИЕ ПАПОК ==============
    
    folders = [
        "pages",
        "tests",
        "data",
        "screenshots",
        "reports",
        "videos"
    ]
    
    print("📁 Создание папок...")
    for folder in folders:
        Path(folder).mkdir(exist_ok=True)
        print(f"   ✅ {folder}/")
    
    # ============== СОЗДАНИЕ __init__.py ==============
    
    print("\n📄 Создание __init__.py файлов...")
    init_files = ["pages/__init__.py", "tests/__init__.py"]
    
    for file_path in init_files:
        Path(file_path).touch()
        print(f"   ✅ {file_path}")
    
    # ============== СОЗДАНИЕ И ЗАПОЛНЕНИЕ ФАЙЛОВ ==============
    
    print("\n📝 Создание и заполнение файлов...")
    
    files = {
        
        # pytest.ini
        "pytest.ini": """[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*

markers =
    smoke: критичные smoke-тесты
    regression: полный регресс
    login: тесты авторизации
    products: тесты товаров

addopts = 
    -v
    -s
    --tb=short
    --html=reports/report.html
    --self-contained-html
""",
        
        # requirements.txt
        "requirements.txt": """playwright==1.40.0
pytest==7.4.3
pytest-playwright==0.4.3
pytest-html==4.1.1
pytest-xdist==3.5.0
requests==2.31.0
""",
        
        # .gitignore
        ".gitignore": """# Python
__pycache__/
*.py[cod]
venv/
env/

# Playwright
screenshots/
videos/
reports/
.pytest_cache/

# IDE
.vscode/
.idea/
""",
        
        # README.md
        "README_structure_created.md": """# Playwright Python Project

## Установка
```bash
python -m venv venv
venv\\Scripts\\Activate.ps1
pip install -r requirements.txt
playwright install
```

## Запуск
```bash
pytest
pytest -m smoke
pytest --html=reports/report.html
```
""",
        
        # pages/base_page.py
        "pages/base_page.py": """from playwright.sync_api import Page


class BasePage:
    def __init__(self, page: Page):
        self.page = page
    
    def open(self, url: str):
        self.page.goto(url, wait_until="domcontentloaded")
        print(f"Открыта страница: {url}")
    
    def click(self, selector: str):
        self.page.click(selector)
        print(f"Клик по: {selector}")
    
    def fill(self, selector: str, text: str):
        self.page.fill(selector, text)
        print(f"Заполнено поле: {selector}")
    
    def get_text(self, selector: str) -> str:
        text = self.page.locator(selector).text_content()
        return text
    
    def get_url(self) -> str:
        return self.page.url
    
    def get_title(self) -> str:
        return self.page.title()
    
    def is_visible(self, selector: str) -> bool:
        return self.page.locator(selector).is_visible()
    
    def wait_for_selector(self, selector: str, timeout: int = 10000):
        self.page.wait_for_selector(selector, timeout=timeout)
    
    def screenshot(self, path: str):
        self.page.screenshot(path=path)
        print(f"Скриншот: {path}")
""",
        
        # pages/login_page.py
        "pages/login_page.py": """from pages.base_page import BasePage


class LoginPage(BasePage):
    
    # Локаторы
    URL = "https://www.saucedemo.com/"
    USERNAME_INPUT = "#user-name"
    PASSWORD_INPUT = "#password"
    LOGIN_BUTTON = "#login-button"
    ERROR_MESSAGE = "h3[data-test='error']"
    
    def open_login_page(self):
        self.open(self.URL)
    
    def enter_username(self, username: str):
        self.fill(self.USERNAME_INPUT, username)
    
    def enter_password(self, password: str):
        self.fill(self.PASSWORD_INPUT, password)
    
    def click_login(self):
        self.click(self.LOGIN_BUTTON)
    
    def login(self, username: str, password: str):
        print(f"Попытка входа: {username}")
        self.enter_username(username)
        self.enter_password(password)
        self.click_login()
    
    def get_error_message(self) -> str:
        return self.get_text(self.ERROR_MESSAGE)
    
    def is_error_visible(self) -> bool:
        return self.is_visible(self.ERROR_MESSAGE)
""",
        
        # tests/conftest.py
        "tests/conftest.py": """import pytest
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
""",
        
        # tests/test_login.py
        "tests/test_login.py": """import pytest


@pytest.mark.smoke
@pytest.mark.login
class TestLogin:
    
    def test_successful_login(self, login_page, valid_user):
        print("ТЕСТ: Успешная авторизация")
        
        login_page.open_login_page()
        
        login_page.login(
            username=valid_user["username"],
            password=valid_user["password"]
        )
        
        assert "/inventory.html" in login_page.get_url()
        print("ТЕСТ ПРОЙДЕН!")
    
    
    @pytest.mark.login
    def test_login_wrong_password(self, login_page):
        print("ТЕСТ: Неверный пароль")
        
        login_page.open_login_page()
        login_page.login("standard_user", "wrong_password")
        
        assert login_page.is_error_visible()
        assert "do not match" in login_page.get_error_message()
        print("ТЕСТ ПРОЙДЕН!")
    
    
    @pytest.mark.login
    def test_login_empty_fields(self, login_page):
        print("ТЕСТ: Пустые поля")
        
        login_page.open_login_page()
        login_page.click_login()
        
        assert login_page.is_error_visible()
        assert "Username is required" in login_page.get_error_message()
        print("ТЕСТ ПРОЙДЕН!")
""",
        
        # data/test_users.json
        "data/test_users.json": """{
"valid_users": [
    {
    "username": "standard_user",
    "password": "secret_sauce"
    }
],
"invalid_users": [
    {
    "username": "locked_out_user",
    "password": "secret_sauce",
    "expected_error": "locked out"
    }
    ]
}
"""
    }
    
    # Записать файлы
    for filepath, content in files.items():
        file = Path(filepath)
        file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(file, "w", encoding="utf-8") as f:
            f.write(content)
        
        print(f"   ✅ {filepath}")
    
    # Итого
    print("\n" + "="*60)
    print("🎉 ПРОЕКТ УСПЕШНО СОЗДАН!")
    print("="*60)
    print("\n📋 Следующие шаги:\n")
    print("1. python -m venv venv")
    print("2. venv\\Scripts\\Activate.ps1")
    print("3. pip install -r requirements.txt")
    print("4. playwright install")
    print("5. pytest\n")


if __name__ == "__main__":
    create_project_structure()
