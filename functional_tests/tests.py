# http://www.obeythetestinggoat.com/book/chapter_explicit_waits_1.html
# todo clean up after FT runs
# todo remove time.sleeps

from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time


class NewVisitorTest(LiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def check_for_row_in_list_table(self, row_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])

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
        time.sleep(1)

        self.check_for_row_in_list_table('1: milk')

        # there is still a text boy for more items.  user enters a second item "sun tan lotion"
        input_box = self.browser.find_element_by_id('id_new_item')
        input_box.send_keys('sun tan lotion')
        input_box.send_keys(Keys.ENTER)
        time.sleep(1)

        # the page updates again, and now shows both items on the list
        self.check_for_row_in_list_table('2: sun tan lotion')
        self.check_for_row_in_list_table('1: milk')

        # the site has generated a unique url for the list.  text is displayed to explain
        self.fail('working, but test not finished')

        # the unique url is navigated to and the list is still there with both items
