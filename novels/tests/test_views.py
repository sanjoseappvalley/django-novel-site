from django.test import TestCase
from novels.models import Novel, Chapter, Story
import datetime
from django.utils import timezone


def create_novel(novel_name):
    return Novel.objects.create(novel_name=novel_name)


class HomePageTest(TestCase):

    def test_uses_home_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')

    def test_current_novels(self):
        novel = create_novel("Heaven Daos")
        response = self.client.get('/')
        self.assertQuerysetEqual(
            response.context['current_novel_list'],
            [novel],
        )

    def test_no_novel(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No novels are available. Please check back later.")
        self.assertQuerysetEqual(response.context['current_novel_list'], [])


class NovelViewTest(TestCase):

    def test_displays_all_chapters(self):
        fno = create_novel("fno")
        fchapter = Chapter(novel=fno, chapter_name='first_ch')
        schapter = Chapter(novel=fno, chapter_name='second_ch')
        fchapter.save()
        schapter.save()
        response = self.client.get(f'/{fno.slug}/')
        self.assertContains(response, fchapter.chapter_name)
        self.assertContains(response, schapter.chapter_name)

    def test_use_novel_template(self):
        novel = create_novel("Demon")
        response = self.client.get(f'/{novel.slug}/')
        self.assertTemplateUsed(response, 'novel.html')

    def test_display_chapters_for_only_that_novel(self):
        fno = create_novel('love story')
        sno = create_novel('bad story')
        fno.chapter_set.create(chapter_name='fnoChap')
        sno.chapter_set.create(chapter_name='snoChap')
        response = self.client.get(f'/{fno.slug}/')
        self.assertContains(response, 'fnoChap')
        self.assertNotContains(response, 'snoChap')

class ChapterViewTest(TestCase):

    def test_access_to_chapter(self):
        aNovel = create_novel('Martial Peak')
        aNovel_chapter = Chapter.objects.create(novel=aNovel, chapter_name='Yang Kai')
        content = Story()
        content.chapter = aNovel_chapter
        content.title = aNovel_chapter.chapter_name
        content.text = 'few paragraphs and spaces between'
        content.save()
        response = self.client.get(f'/{aNovel.slug}/{aNovel_chapter.slug}/')
        self.assertEqual(response.status_code, 200)

    def test_use_chapter_template(self):
        aNovel = create_novel('GDG')
        chapter = Chapter.objects.create(novel=aNovel, chapter_name='Mo Sheng')
        response = self.client.get(f'/{aNovel.slug}/{chapter.slug}/')
        self.assertTemplateUsed(response, 'chapter.html')


    def test_displays_default_content(self):
        aNovel = create_novel('GDG')
        chapter1 = Chapter.objects.create(novel=aNovel, chapter_name='Mo Sheng')
        chapter1.story_set.create(title=chapter1.chapter_name)
        response = self.client.get(f'/{aNovel.slug}/{chapter1.slug}/')
        self.assertContains(response, 'chapter story')

    def test_displays_written_content(self):
        aNovel = create_novel('GDG')
        chapter1 = Chapter.objects.create(novel=aNovel, chapter_name='Mo Sheng')
        chapter1.story_set.create(title='p1', text='Great Demon God')
        chapter1.story_set.create(title='p2', text='Mo Sheng is.')
        chapter1.story_set.create(title='p3', text='Golden left eye')
        response = self.client.get(f'/{aNovel.slug}/{chapter1.slug}/')
        self.assertContains(response, 'Great Demon God')
        self.assertContains(response, 'Mo Sheng is.')
        self.assertContains(response, 'Golden left eye')
