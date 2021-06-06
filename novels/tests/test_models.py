from django.test import TestCase
from novels.models import Novel
import datetime
from django.utils import timezone


def create_novel(novel_name, days):
    time = timezone.now() + datetime.timedelta(days)
    return Novel.objects.create(novel_name=novel_name, release_date=time)


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
