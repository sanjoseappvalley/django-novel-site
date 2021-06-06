from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
import time


class NewVisitorTest(StaticLiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_can_choose_a_novel_to_read(self):
        # Nick has heard about a novel site. He goes to check it out
        self.browser.get('http://localhost:8000')

        # He notices the page title and header mention heaven daos
        self.assertIn('Immortal Mansion', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('Immortal Mansion', header_text)
        # He sees a list of novels that he can choose to read
        novels = self.browser.find_elements_by_tag_name('li')
        self.assertTrue(
            any(novel.text == 'Legend of Chusen' for novel in novels),
            "There is no novel with such name!"
        )
        # He clicks on the first novel
        self.browser.find_element_by_link_text("Legend of Chusen").click()
        time.sleep(2)
        # The page moves to the novel page, and he sees the title and a list of chapters
        novel_name = self.browser.find_element_by_tag_name('h1').text
        self.assertEqual(novel_name, "Legend of Chusen")
        # first_novel_url = self.browser.current_url
        # self.assertContains(first_novel_url, novel_name)
        chapters = self.browser.find_element_by_tag_name('li')
        self.assertTrue(
            any(chapter.text == 'Chapter 1: Zhang Xiao Fan' for chapter in chapters),
            "Chapter name doesn't match!"
        )
        # he clicks on chapter 1 and the page changes to chapter 1 content page
        self.browser.find_element_by_partial_link_text("Chapter 1:").click()
        time.sleep(2)
        # He sees chapter 1 content and starts reading
        self.assertEqual(self.browser.find_element_by_tag_name('h1').text, "Zhang Xiao Fan")
        # finishing chapter 1 he sees the next button, he clicks on it
        self.fail(msg='Finish the test!')
        # the page moves to chapter 2 and he continues reading
