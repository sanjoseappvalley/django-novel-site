from django.test import TestCase
from novels.models import Novel
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
        response = self.client.get(f'/{fno.novel_name}/')
        self.assertEqual(response.status_code, 200)

    # def test_use_novel_template(self):
    #     novel = create_novel("Demon", 0)
    #     response = self.client.get(f'/{novel.novel_name}/')
    #     self.assertTemplateUsed(response, 'novel.html')
