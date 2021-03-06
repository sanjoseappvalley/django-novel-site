from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
import time, os
from novels.models import Novel
from django.utils import timezone


class NewVisitorTest(StaticLiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        staging_server = os.environ.get('STAGING_SERVER')
        if staging_server:
            self.live_server_url = 'http://' + staging_server
        self.fno = Novel(novel_name="Demons Among Gods")
        self.fno.save()
        self.fno.chapter_set.create(chapter_name='Chapter 1: Ancient Tales')
        self.c2 = self.fno.chapter_set.create(chapter_name='Chapter 2: Heated Battles', content='chapter 2 story line')
        

    def tearDown(self):
        self.browser.quit()

    def test_can_choose_a_novel_to_read(self):
        # Nick has heard about a novel site. He goes to check it out
        self.browser.get(self.live_server_url)
        time.sleep(2)
        # He notices the page title and header mention heaven daos
        self.assertIn('Immortal Mansion', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertEqual('Immortal Mansion', header_text)

        # He sees a list of novels that he can choose to read
        novels = self.browser.find_elements_by_tag_name('li')
        # self.assertTrue(
        #     any(novel.text == 'Legend of Chusen' for novel in novels),
        #     "There is no novel with such name!"
        # )
        self.assertIn('Demons Among Gods', [novel.text for novel in novels])
        # He clicks on the first novel
        self.browser.find_element_by_link_text('Demons Among Gods').click()
        time.sleep(2)
        # The page moves to the novel page, and he sees the title and a list of chapters
        novel_name = self.browser.find_element_by_tag_name('h1').text
        self.assertEqual(novel_name, 'Demons Among Gods')
        first_novel_url = self.browser.current_url
        # the url has the novel name with - at the end
        self.assertIn("demons-among-gods", first_novel_url)
        chapters = self.browser.find_elements_by_tag_name('li')
        self.assertTrue(
            any(chapter.text == 'Chapter 1: Ancient Tales' for chapter in chapters),
            "No chapter name matches!"
        )
        # he clicks on chapter 1 and the page changes to chapter 1 content page
        self.browser.find_element_by_partial_link_text("Chapter 1:").click()
        time.sleep(2)
        # He sees chapter 1 content and starts reading
        self.assertEqual(self.browser.find_element_by_tag_name('h1').text, "Chapter 1: Ancient Tales")
        # finishing chapter 1 he sees the next button, he clicks on it
        self.browser.find_element_by_link_text("Next Chapter").click()
        time.sleep(2)
        self.assertEqual(self.browser.find_element_by_tag_name('h1').text, 'Chapter 2: Heated Battles')
        # he's reading chapter 2
        self.assertIn(self.browser.find_element_by_tag_name('p').text, 'chapter 2 story line')
        # After reading chapter 2, Nick realizes that he wants to comment on the story, so he Register
        # for an account
        self.browser.find_element_by_link_text('Register').click()
        time.sleep(2)
        self.browser.find_element_by_id('id_username').send_keys('bbb')
        self.browser.find_element_by_id('id_email').send_keys('bbb@gmail.com')
        self.browser.find_element_by_id('id_password1').send_keys('bbbb1234')
        self.browser.find_element_by_id('id_password2').send_keys('bbbb1234')
        self.browser.find_element_by_name('button').click()
        time.sleep(2)
        self.assertEqual(self.browser.find_element_by_class_name('alert').text, "Account created for bbb!")
        # continue

        # self.fail(msg='Finish the test!')
        # the page moves to chapter 2 and he continues reading
