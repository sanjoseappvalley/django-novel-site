from django.test import TestCase
from novels.models import Novel, Chapter
import datetime
from django.utils import timezone
from django.core.exceptions import ValidationError


def create_novel(novel_name):
    return Novel.objects.create(novel_name=novel_name)


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

    def test_get_absolute_url(self):
        novel = create_novel("test novel")
        self.assertEqual(novel.get_absolute_url(), f'/test-novel/')

    def test_create_novel_and_first_chapter(self):
        fno = create_novel('Gods of war')
        chapter = fno.chapter_set.create(chapter_name='chapter1st')
        self.assertEqual(fno, chapter.novel)
        self.assertEqual(fno.chapter_set.first().chapter_name, 'chapter1st')


class ChapterModelTest(TestCase):

    def test_default_name(self):
        chapter = Chapter()
        self.assertEqual(chapter.chapter_name, '')

    def test_chapter_is_related_to_novel(self):
        novel_ = Novel()
        novel_.save()
        chapter_ = Chapter()
        chapter_.novel = novel_
        chapter_.save()
        self.assertIn(chapter_, novel_.chapter_set.all())

    def test_duplicate_items_are_invalid(self):
        fno = Novel.objects.create()
        Chapter.objects.create(novel=fno, chapter_name='chapter1')
        with self.assertRaises(ValidationError):
            chapter = Chapter(novel=fno, chapter_name='chapter1')
            chapter.full_clean()
