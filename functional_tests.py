import unittest
from selenium import webdriver


class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_can_choose_a_novel_to_read(self):
        # Nick has heard about a novel site. He goes to check it out
        self.browser.get('http://localhost:8000')

        # He notices the page title and header mention heaven daos
        self.assertIn('Heaven Daos', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('Heaven Daos', header_text)
        # He sees a list of novels that he can choose to read
        novels = self.browser.find_elements_by_tag_name('article')
        self.assertTrue(
            any(novel.text == 'Chusen' for novel in novels),
            "There is no novel with such name"
        )
        # He clicks on the first novel Martial Peak
        self.fail(msg='Finish the test!')
        # The page moves to Martial Peak detail page, now he sees numbers of
        # chapters to choose from

        # he clicks on chapter 1 and the page changes to chapter 1 content page

        # He sees chapter 1 content and starts reading

        # finishing chapter 1 he sees the next button, he clicks on it

        # the page moves to chapter 2 and he continues reading


if __name__ == "__main__":
    unittest.main()
