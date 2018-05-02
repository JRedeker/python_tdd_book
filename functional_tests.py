# http://www.obeythetestinggoat.com/book/chapter_02_unittest.html
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest


class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_can_start_list_and_retrieve_later(self):
        # user opens the website
        self.browser.get('http://localhost:8000')

        # the page loads and sees the title
        self.assertIn('Remember', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('Remember', header_text)

        # user is invited to enter a first remember item
        input_box = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
            input_box.get_attribute('placeholder'),
            'Enter an item to remember'
        )

        # user enters a first remember item of "swimsuit"
        input_box.send_keys('swimsuit')

        # when the user hits enter, the page updates, and the page now lists:
        # "1: buy swimsuit for vacation"
        input_box.send_keys(Keys.ENTER)
        time.sleep(1)

        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_element_by_tag_name('tr')
        self.assertTrue(any(row.text == '1: swimsuit' for row in rows))

        # there is still a text boy for more items.  user enters a second item "sun tan lotion"
        self.fail('working, but test not finished')

        # the page updates again, and now shows both items on the list

        # the site has generated a unique url for the list.  text is displayed to explain

        # the unique url is navigated to and the list is still there with both items


if __name__ == '__main__':
    unittest.main(warnings='ignore')
