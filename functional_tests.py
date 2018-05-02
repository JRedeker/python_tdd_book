# http://www.obeythetestinggoat.com/book/chapter_02_unittest.html
from selenium import webdriver
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
        self.fail('test not complete')

        # user is invited to enter a first remember item

        # user enters a first remember item of "swimsuit"

        # when the user hits enter, the page updates, and the page now lists:
        # "1: buy swimsuit for vacation"

        # there is still a text boy for more items.  user enters a second item "sun tan lotion"

        # the page updates again, and now shows both items on the list

        # the site has generated a unique url for the list.  text is displayed to explain

        # the unique url is navigated to and the list is still there with both items


if __name__ == '__main__':
    unittest.main(warnings='ignore')
