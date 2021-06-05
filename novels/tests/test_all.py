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


class NovelModelTest(TestCase):

    def test_saving_and_retrieving_novels(self):
        first_novel = Novel()
        first_novel.novel_name = "FNO"
        first_novel.release_date = timezone.now()
        first_novel.save()

        second_novel = Novel()
        second_novel.novel_name = "SNO"
        second_novel.release_date = timezone.now()
        second_novel.save()

        saved_novels = Novel.objects.all()
        self.assertEqual(saved_novels.count(), 2)

        fno = saved_novels[0]
        sno = saved_novels[1]
        self.assertEqual(fno.novel_name, "FNO")
        self.assertEqual(sno.novel_name, "SNO")

    # def test_get_absolute_url(self):
    #     novel = create_novel("testnovel", 0)
    #     self.assertEqual(novel.get_absolute_url(), f'/{novel.novel_name}/')


# class NovelViewTest(TestCase):

#     def test_displays_all_chapters(self):

    # def test_use_novel_template(self):
    #     novel = create_novel("Demon", 0)
    #     response = self.client.get(f'/{novel.novel_name}/')
    #     self.assertTemplateUsed(response, 'novel.html')
