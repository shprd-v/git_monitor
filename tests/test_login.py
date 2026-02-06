import pytest


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
