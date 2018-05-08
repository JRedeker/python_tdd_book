# http://www.obeythetestinggoat.com/book/chapter_explicit_waits_1.html
# todo clean up after FT runs

from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
import time

MAX_WAIT = 10


class NewVisitorTest(LiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def wait_for_row_in_list_table(self, row_text):
        start_time = time.time()
        while True:
            try:
                table = self.browser.find_element_by_id('id_list_table')
                rows = table.find_elements_by_tag_name('tr')
                self.assertIn(row_text, [row.text for row in rows])
                return
            except (AssertionError, WebDriverException) as exception:
                if time.time() - start_time > MAX_WAIT:
                    raise exception
                time.sleep(0.5)

    def test_can_start_list_and_retrieve_later(self):
        # user opens the website
        self.browser.get(self.live_server_url)

        # the page loads and sees the title
        self.assertIn('Grocery List', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('Grocery List', header_text)

        # user is invited to enter a first Grocery List item
        input_box = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
            input_box.get_attribute('placeholder'),
            'Enter a grocery list item'
        )

        # user enters a first Grocery List item of "swimsuit"
        input_box.send_keys('milk')

        # when the user hits enter, the page updates, and the page now lists:
        # "1: buy swimsuit for vacation"
        input_box.send_keys(Keys.ENTER)

        self.wait_for_row_in_list_table('1: milk')

        # there is still a text boy for more items.  user enters a second item "sun tan lotion"
        input_box = self.browser.find_element_by_id('id_new_item')
        input_box.send_keys('sun tan lotion')
        input_box.send_keys(Keys.ENTER)

        # the page updates again, and now shows both items on the list
        self.wait_for_row_in_list_table('2: sun tan lotion')
        self.wait_for_row_in_list_table('1: milk')

        # the site has generated a unique url for the list.  text is displayed to explain
        current_url = self.browser.current_url
        self.assertRegex(current_url, '/lists/.+')

        # the unique url is navigated to and the list is still there with both items
        page_text = self.browser.find_elements_by_tag_name('body').text
        self.assertIn('milk', page_text)
        self.assertIn('sun tan lotion', page_text)

    def test_multiple_users_can_start_lists_at_different_urls(self):
        # user one starts a new grocery list
        self.browser.get(self.live_server_url)
        input_box = self.browser.find_element_by_id('id_new_item')
        input_box.send_keys('cookies')
        input_box.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: cookies')

        # user one notices the unique url
        user_one_list_url = self.browser.current_url
        self.assertRegex(user_one_list_url, '/lists/.+')

        # user two begins
        self.browser.quit()
        self.browser = webdriver.Firefox()

        # user two visits the home page, and the page is cleaned up
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_elements_by_tag_name('body').text
        self.assertNotIn('cookies', page_text)
        self.assertNotIn('sun tan lotion', page_text)

        # user two enters in their own first item
        input_box = self.browser.find_elements_by_id('id_new_item')
        input_box.send_keys('eggs')
        input_box.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1. eggs')

        # user two gets own unique url
        user_two_list_url = self.browser.current_url
        self.assertRegex(user_two_list_url, '/lists/.+')
        self.assertNotEqual(user_two_list_url, user_one_list_url)

        # there is still no trace of user ones list items
        page_text = self.browser.find_elements_by_tag_name('body').text
        self.assertNotIn('cookies', page_text)
        self.assertNotIn('sun tan lotion', page_text)
