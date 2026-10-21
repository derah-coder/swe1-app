from datetime import timedelta

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import Question


def create_question(question_text, days=0):
    """Create a question published `days` from now (negative for the past)."""
    pub_date = timezone.now() + timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=pub_date)


class QuestionModelTests(TestCase):
    def test_was_published_recently_with_recent_question(self):
        question = Question(pub_date=timezone.now() - timedelta(hours=1))
        self.assertIs(question.was_published_recently(), True)

    def test_was_published_recently_with_old_question(self):
        question = Question(pub_date=timezone.now() - timedelta(days=2))
        self.assertIs(question.was_published_recently(), False)

    def test_was_published_recently_with_future_question(self):
        question = Question(pub_date=timezone.now() + timedelta(days=2))
        self.assertIs(question.was_published_recently(), False)


class IndexViewTests(TestCase):
    def test_no_questions(self):
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")

    def test_lists_question(self):
        create_question("What's new?")
        response = self.client.get(reverse("polls:index"))
        self.assertContains(response, "What&#x27;s new?")


class VoteViewTests(TestCase):
    def test_vote_counts_and_redirects_to_results(self):
        question = create_question("Favorite color?")
        choice = question.choice_set.create(choice_text="Blue")
        response = self.client.post(
            reverse("polls:vote", args=(question.id,)), {"choice": choice.id}
        )
        self.assertRedirects(response, reverse("polls:results", args=(question.id,)))
        choice.refresh_from_db()
        self.assertEqual(choice.votes, 1)

    def test_vote_without_choice_shows_error(self):
        question = create_question("Favorite color?")
        response = self.client.post(reverse("polls:vote", args=(question.id,)))
        self.assertContains(response, "Please select an answer.")
