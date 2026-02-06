from playwright.sync_api import Page


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
