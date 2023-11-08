import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from .models import Subject

def create_subject(subject_text, days):
    """
    Create a subject with the given `subject_text` and published the
    given number of `days` offset to now (negative for subjects published
    in the past, positive for subjects that have yet to be published).
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Subject.objects.create(subject_text=subject_text, pub_date=time)

class SubjectDetailViewTests(TestCase):
    def test_future_subject(self):
        """
        The detail view of a subject with a pub_date in the future
        returns a 404 not found.
        """
        future_subject = create_subject(subject_text="Future subject.", days=5)
        url = reverse("subjects:detail", args=(future_subject.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_subject(self):
        """
        The detail view of a subject with a pub_date in the past
        displays the subject's text.
        """
        past_subject = create_subject(subject_text="Past subject.", days=-5)
        url = reverse("subjects:detail", args=(past_subject.id,))
        response = self.client.get(url)
        self.assertContains(response, past_subject.subject_text)

class SubjectIndexViewTests(TestCase):
    def test_no_subjects(self):
        """
        If no subjects exist, an appropriate message is displayed.
        """
        response = self.client.get(reverse("subjects:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerySetEqual(response.context["latest_subject_list"], [])

    def test_past_subject(self):
        """
        subjects with a pub_date in the past are displayed on the
        index page.
        """
        subject = create_subject(subject_text="Past subject.", days=-30)
        response = self.client.get(reverse("subjects:index"))
        self.assertQuerySetEqual(
            response.context["latest_subject_list"],
            [subject],
        )

    def test_future_subject(self):
        """
        subjects with a pub_date in the future aren't displayed on
        the index page.
        """
        create_subject(subject_text="Future subject.", days=30)
        response = self.client.get(reverse("subjects:index"))
        self.assertContains(response, "No polls are available.")
        self.assertQuerySetEqual(response.context["latest_subject_list"], [])

    def test_future_subject_and_past_subject(self):
        """
        Even if both past and future subjects exist, only past subjects
        are displayed.
        """
        subject = create_subject(subject_text="Past subject.", days=-30)
        create_subject(subject_text="Future subject.", days=30)
        response = self.client.get(reverse("subjects:index"))
        self.assertQuerySetEqual(
            response.context["latest_subject_list"],
            [subject],
        )

    def test_two_past_subjects(self):
        """
        The subjects index page may display multiple subjects.
        """
        subject1 = create_subject(subject_text="Past subject 1.", days=-30)
        subject2 = create_subject(subject_text="Past subject 2.", days=-5)
        response = self.client.get(reverse("subjects:index"))
        self.assertQuerySetEqual(
            response.context["latest_subject_list"],
            [subject2, subject1],
        )

class SubjectModelTests(TestCase):
    def test_was_published_recently_with_future_subject(self):
        """
        was_published_recently() returns False for subjects whose pub_date
        is in the future.
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_subject = Subject(pub_date=time)
        self.assertIs(future_subject.was_published_recently(), False)
        
    def test_was_published_recently_with_old_subject(self):
        """
        was_published_recently() returns False for subjects whose pub_date
        is older than 1 day.
        """
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_subject = Subject(pub_date=time)
        self.assertIs(old_subject.was_published_recently(), False)


    def test_was_published_recently_with_recent_subject(self):
        """
        was_published_recently() returns True for subjects whose pub_date
        is within the last day.
        """
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_subject = Subject(pub_date=time)
        self.assertIs(recent_subject.was_published_recently(), True)