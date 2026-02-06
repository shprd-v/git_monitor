from pages.base_page import BasePage


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
