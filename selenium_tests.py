from selenium import webdriver
import unittest


class TestCalculator(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Chrome()

    def tearDown(self):
        self.browser.quit()

    def test_title(self):
        self.browser.get("http://localhost:5000/")
        self.assertEqual(self.browser.title, "Podcast Radio")

    def test_welcome(self):
        self.browser.get("http://localhost:5000/")

        btn_signup = self.browser.find_element_by_id("sign_up")

        btn_login = self.browser.find_element_by_id("login")

        btn_listen = self.browser.find_element_by_id("listen")

    def test_signup(self):
        """tests sign up process"""

        self.browser.get("http://localhost:5000/signup")

        name = self.browser.find_element_by_id("name")
        name.send_keys("Sally")

        email = self.browser.find_element_by_id("email")
        email.send_keys("sally@gmail.com")

        password = self.browser.find_element_by_id("password")
        password.send_keys("sally")

        btn_submit = self.browser.find_element_by_id("submit")

    def test_login(self):
        """tests log in process"""

        self.browser.get("http://localhost:5000/login")

        email = self.browser.find_element_by_id("email")
        email.send_keys("sally@gmail.com")

        password = self.browser.find_element_by_id("password")
        password.send_keys("sally")

        btn_submit = self.browser.find_element_by_id("submit")

    def test_listen(self):
        """tests listening page"""

        self.browser.get("http://localhost:5000/podcasts")

        listen = self.browser.find_element_by_name("News")


if __name__ == "__main__":
    unittest.main()
