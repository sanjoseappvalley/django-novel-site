from django.test import TestCase
from novels.models import Novel, Chapter
import datetime
from django.utils import timezone


def create_novel(novel_name, days):
    time = timezone.now() + datetime.timedelta(days)
    return Novel.objects.create(novel_name=novel_name, release_date=time)


class HomePageTest(TestCase):

    def test_uses_home_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')

    def test_current_novels(self):
        novel = create_novel("Heaven Daos", 0)
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
        fno = create_novel("fno", 0)
        fchapter = Chapter(novel=fno, chapter_name='first_ch')
        schapter = Chapter(novel=fno, chapter_name='second_ch')
        fchapter.save()
        schapter.save()
        response = self.client.get(f'/{fno.slug}/')
        self.assertContains(response, fchapter.chapter_name)
        self.assertContains(response, schapter.chapter_name)

    def test_use_novel_template(self):
        novel = create_novel("Demon", 0)
        response = self.client.get(f'/{novel.slug}/')
        self.assertTemplateUsed(response, 'novel.html')

    def test_display_chapters_for_only_that_novel(self):
        fno = create_novel('love story', 0)
        sno = create_novel('bad story', 0)
        fno.chapter_set.create(chapter_name='fnoChap')
        sno.chapter_set.create(chapter_name='snoChap')
        response = self.client.get(f'/{fno.slug}/')
        self.assertContains(response, 'fnoChap')
        self.assertNotContains(response, 'snoChap')
