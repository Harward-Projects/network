from django.test import TestCase, Client
from selenium import webdriver
from .models import User, Post

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# from django.contrib.auth.models import User

# db.connection.set_schema("test")


# class FunctionalTestClass(TestCase):

#     def setUp(self):
#         self.browser = webdriver.Chrome()

#     def test_01(self):
#         user = User.objects.create_user(
#             username="tester01", email="tester01@example.com", password="password"
#         )
#         user.save()
#         self.browser.get("http://127.0.0.1:8000/")
#         self.browser.find_element(By.LINK_TEXT, "Log In").click()
#         username = self.browser.find_element(By.NAME, "username")
#         username.send_keys("tester01")
#         password = self.browser.find_element(By.NAME, "password")
#         password.send_keys("password")
#         self.browser.find_element("css selector", ".btn.btn-primary").click()

#         wait = WebDriverWait(self.browser, 10)  # Wait up to 10 seconds
#         post = wait.until(EC.presence_of_element_located((By.ID, "id_content")))
#         # post = self.browser.find_element(By.ID, "id_content")
#         post.send_keys("The New New Test Text by tester01 user")
#         self.browser.find_element("id", "submitPost").click()
#         self.assertIn("Test text", self.browser.page_source)

#     def tearDown(self):
#         time.sleep(10)
#         self.browser.quit()


class UnitTestClass(TestCase):

    def setUp(self):
        pass

    def test_assess_response_from_index_url(self):
        user = User.objects.create_user(
            username="tester01", email="tester01@example.com", password="password"
        )
        user.save()
        self.assertEqual(user.username, "tester01")

        # self.client.force_login(user)

        post = Post.objects.create(
            author=user, content="the very new content for test only after force_login"
        )
        post.save()

        response = self.client.get("")
        # self.assertEqual(response.content, "new")
        print(response.content)
        print(type(response))

        self.assertContains(response, "new")

        # client = Client()
        # response = client.get("/")
        # self.assertEqual(response.status_code, 200)


# if __name__ == "__main__":
#     unittest.main()
