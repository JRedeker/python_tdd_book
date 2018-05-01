# http://www.obeythetestinggoat.com/book/chapter_02_unittest.html
from selenium import webdriver

# user opens the website
browser = webdriver.Firefox()
browser.get('http://localhost:8000')

# the page loads and sees the header
assert 'Remember' in browser.title

# user is invited to enter a first remember item

# user enters a first remember item of "swimsuit"

# when the user hits enter, the page updates, and the page now lists:
# "1: buy swimsuit for vacation"

# there is still a text boy for more items.  user enters a second item "sun tan lotion"

# the page updates again, and now shows both items on the list

# the site has generated a unique url for the list.  text is displayed to explain

# the unique url is navigated to and the list is still there with both items

