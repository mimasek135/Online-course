from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from datetime import date
from .models import Course, Question, Choice, Submission

class ExamTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user('learner', password='test-pass')
        self.other = get_user_model().objects.create_user('other', password='other-pass')
        self.course = Course.objects.create(name='Django', description='Test', pub_date=date.today())
        self.q = Question.objects.create(course=self.course, content='Choose both', grade=10)
        self.a = Choice.objects.create(question=self.q, content='A', is_correct=True)
        self.b = Choice.objects.create(question=self.q, content='B', is_correct=True)
        self.wrong = Choice.objects.create(question=self.q, content='C', is_correct=False)
        self.url = reverse('onlinecourse:submit', args=[self.course.pk])
        self.client.force_login(self.user)
    def test_success_and_result(self):
        response = self.client.post(self.url, {'choice': [self.a.pk, self.b.pk]}, follow=True)
        self.assertContains(response, 'Congratulations!')
        self.assertEqual(response.context['score'], 100)
    def test_partial_or_extra_answers_get_no_points(self):
        for ids in [[self.a.pk], [self.a.pk, self.b.pk, self.wrong.pk], []]:
            response = self.client.post(self.url, {'choice': ids}, follow=True)
            self.assertEqual(response.context['score'], 0)
    def test_foreign_or_invalid_choices_are_rejected(self):
        other_course = Course.objects.create(name='Other', description='Other', pub_date=date.today())
        question = Question.objects.create(course=other_course, content='Foreign')
        foreign = Choice.objects.create(question=question, content='Foreign', is_correct=True)
        for value in [str(foreign.pk), 'abc', '999999']:
            self.assertEqual(self.client.post(self.url, {'choice': [value]}).status_code, 400)
        self.assertEqual(Submission.objects.count(), 0)
    def test_result_is_private(self):
        response = self.client.post(self.url, {'choice': [self.a.pk, self.b.pk]})
        self.client.force_login(self.other)
        self.assertEqual(self.client.get(response.url).status_code, 404)
    def test_post_and_login_required(self):
        self.assertEqual(self.client.get(self.url).status_code, 405)
        self.client.logout()
        self.assertEqual(self.client.post(self.url).status_code, 302)
    def test_csrf_is_required(self):
        from django.test import Client
        client = Client(enforce_csrf_checks=True)
        client.force_login(self.user)
        self.assertEqual(client.post(self.url, {'choice': [self.a.pk]}).status_code, 403)
